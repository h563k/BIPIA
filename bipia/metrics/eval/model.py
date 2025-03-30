# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import Callable, Dict
import yaml
import time
import re
import os
import openai

from accelerate.logging import get_logger
from openai import (
    RateLimitError,
    Timeout,
    APIConnectionError,
    APIError,
)

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from .base import BaseEval

logger = get_logger(__name__)


def get_retry_time(err_info):
    z = re.search(r"after (\d+) seconds", err_info)
    if z:
        return int(z.group(1))
    return 1


class ModelEval(BaseEval):
    """Compute evaluate metrics with GPT4"""

    def __init__(self, config: str | dict, judge_fn: Callable, format_fn: Callable):
        super().__init__()

        self.config = self.load_config(config)

        self.judge_fn = judge_fn
        self.format_fn = format_fn

    def load_config(self, config: str | dict) -> Dict:
        if isinstance(config, dict):
            return config
        with open(config, "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        return config

    def env_init(self):
        proxy = self.config.get("proxy", None)
        if proxy:
            os.environ['http_proxy'] = proxy
            os.environ['https_proxy'] = proxy
            os.environ['ftp_proxy'] = proxy
            os.environ['no_proxy'] = '127.0.0.1,localhost'
            os.environ['HTTP_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy
            os.environ['FTP_PROXY'] = proxy
            os.environ['NO_PROXY'] = '127.0.0.1,localhost'

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(0))
    def chat_completion(
        self,
        messages,
        temperature=None,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0,
    ):
        success = False
        self.env_init()
        while not success:
            try:
                api_key = self.config.get("api_key", None)
                base_url = self.config.get("api_base", None)
                client = openai.OpenAI(api_key=api_key, base_url=base_url)
                response = client.chat.completions.create(
                    model=self.config.get("model", None),
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stream=True,
                )
                success = True
            except RateLimitError as e:
                logger.debug(e, exc_info=True)
                retry_time = get_retry_time(str(e))
                time.sleep(retry_time)
            except Timeout as e:
                logger.debug(e, exc_info=True)
                time.sleep(1)
            except APIConnectionError as e:
                logger.debug(e, exc_info=True)
                time.sleep(1)
            except APIError as e:
                logger.debug(e, exc_info=True)
                time.sleep(1)
            except Exception as e:
                logger.warning(e, exc_info=True)
                success = True
                response = {"choices": []}

        rslts = ""
        try:
            for chunk in response:
                delta = chunk.choices[0].delta.content
                rslts += str(delta)
        except Exception as e:
            logger.warning(e, exc_info=True)
        return [rslts]

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(0))
    def completion(
        self,
        messages,
        temperature=None,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["<|im_end|>"],
    ):
        success = False
        self.env_init()
        while not success:
            try:
                api_key = self.config.get("api_key", None)
                base_url = self.config.get("api_base", None)
                client = openai.OpenAI(api_key=api_key, base_url=base_url)
                response = client.completions.create(
                    model=self.config.get("model", None),
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=stop,
                )
                success = True
            except RateLimitError as e:
                logger.debug(e, exc_info=True)
                retry_time = get_retry_time(str(e))
                time.sleep(retry_time)
            except Timeout as e:
                logger.debug(e, exc_info=True)
                time.sleep(1)
            except APIConnectionError as e:
                logger.debug(e, exc_info=True)
                time.sleep(1)
            except APIError as e:
                logger.debug(e, exc_info=True)
                time.sleep(1)
            except Exception as e:
                logger.warning(e, exc_info=True)
                success = True
                response = {"choices": []}

        rslts = [i["text"] for i in response["choices"]]
        return rslts

    def _compute_score(self, prediction: str = None, **kwargs):
        messages = self.format_fn(prediction, chat=self.config["chat"])

        if self.config["chat"]:
            response = self.chat_completion(
                messages, temperature=0, max_tokens=32)
        else:
            response = self.completion(messages, temperature=0, max_tokens=32)

        if len(response) > 0:
            asr = self.judge_fn(response[0])
        else:
            asr = -1
        return asr

    def _batch_compute_score(self, predictions: str = None, **kwargs):
        messages = [
            self.format_fn(prediction, chat=self.config["chat"])
            for prediction in predictions
        ]

        responses = self.completion(messages, temperature=0, max_tokens=32)

        if len(responses) > 0:
            asrs = [self.judge_fn(response) for response in responses]
        else:
            asrs = [-1] * len(messages)
        return asrs

    def add_batch(self, *, predictions=None, **kwargs):
        if self.config["chat"]:
            batch_asrs = []
            for pred in predictions:
                asr = self._compute_score(prediction=pred)
                batch_asrs.append(asr)

            self.asrs.extend(batch_asrs)
        else:
            batch_asrs = self._batch_compute_score(predictions=predictions)
            self.asrs.extend(batch_asrs)

        return batch_asrs
