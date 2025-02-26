"""LLM caller module."""

import asyncio
import os
import time
from typing import TypeVar

from dotenv import load_dotenv
from litellm import (
    acompletion,
    completion,
    supports_response_schema,
    token_counter,
)
from pydantic import BaseModel

from logger import get_logger

logger = get_logger(__name__)
T = TypeVar("T", bound=BaseModel)


class MinuteRateLimiter:
    """Rate limiter for the LLM."""

    def __init__(self, tokens_per_minute: int) -> None:
        """Initialize the rate limiter.

        Args:
            tokens_per_minute: The number of tokens per minute.
        """
        self.tokens_per_minute = tokens_per_minute
        self.tokens_available = tokens_per_minute
        self.last_refill_time = time.time()

    def _try_acquire(self, tokens: int) -> bool:
        """Try to acquire tokens.

        Args:
            tokens: The number of tokens to acquire.

        Returns:
            True if tokens were acquired, False otherwise.
        """
        now = time.time()
        minutes_passed = (now - self.last_refill_time) / 60.0

        # Refill tokens based on time passed
        self.tokens_available = int(
            min(
                self.tokens_per_minute,
                self.tokens_available + minutes_passed * self.tokens_per_minute,
            )
        )
        self.last_refill_time = now

        if self.tokens_available >= tokens:
            self.tokens_available -= tokens
            return True
        return False

    def acquire(self, tokens: int) -> None:
        """Acquire tokens synchronously.

        Args:
            tokens: The number of tokens to acquire.
        """
        while not self._try_acquire(tokens):
            time.sleep(1)

    async def async_acquire(self, tokens: int) -> None:
        """Acquire tokens asynchronously.

        Args:
            tokens: The number of tokens to acquire.
        """
        while not self._try_acquire(tokens):
            await asyncio.sleep(1)


load_dotenv()
rate_limiter = MinuteRateLimiter(tokens_per_minute=int(os.getenv("MAX_TOKENS_PER_MINUTE", 100000)))


def ask_llm(
    model: str,
    sys_prompt: str,
    user_prompt: str,
    top_p: float = 1,
    temperature: float = 0.5,
) -> tuple[str, float]:
    """Ask the LLM.

    Args:
        model: The model to use.
        sys_prompt: The system prompt.
        user_prompt: The user prompt.
        top_p: The top p value.
        temperature: The temperature value.

    Returns:
        The response from the LLM and the cost of the request.
    """
    logger.info(f"Calling {model} with prompt")
    load_dotenv()

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        rate_limiter.acquire(token_counter(model, messages=messages))
        response = completion(
            model=model,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
        )
        logger.debug("Received successful response")
        return response.model_dump_json(indent=2), response._hidden_params["response_cost"]
    except Exception:
        logger.exception(f"Communication error with {model}")
        raise


def ask_llm_with_schema(
    model: str,
    sys_prompt: str,
    user_prompt: str,
    output_class: type[T],
    top_p: float = 1,
    temperature: float = 0.5,
) -> tuple[T, float]:
    """Ask the LLM enforcing the response adheres to a schema.

    Args:
        model: The model to use.
        sys_prompt: The system prompt.
        user_prompt: The user prompt.
        output_class: The output class.
        top_p: The top p value.
        temperature: The temperature value.

    Returns:
        The response from the LLM and the cost of the request.
    """
    logger.info(f"Calling for {model} with schema")
    load_dotenv()

    if not supports_response_schema(model=model):
        msg = f"Model {model} does not support schemas, use the `ask_llm` function instead"
        logger.error(msg)
        raise ValueError(msg)

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        rate_limiter.acquire(token_counter(model, messages=messages))
        response = completion(
            model=model,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
            response_format=output_class,
        )
        logger.debug("Received successful response")
        content = response.choices[0].message.content
        return output_class.model_validate_json(content), response._hidden_params["response_cost"]
    except Exception:
        logger.exception(f"Communication error with {model}")
        raise


async def ask_llm_async(
    model: str,
    sys_prompt: str,
    user_prompt: str,
    top_p: float = 1,
    temperature: float = 0.5,
) -> tuple[str, float]:
    """Ask the LLM asynchronously.

    Args:
        model: The model to use.
        sys_prompt: The system prompt.
        user_prompt: The user prompt.
        top_p: The top p value.
        temperature: The temperature value.

    Returns:
        The response from the LLM and the cost of the request.
    """
    logger.info(f"Calling {model} with prompt")
    load_dotenv()

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt},
    ]
    await rate_limiter.async_acquire(token_counter(model, messages=messages))
    logger.info("Rate limit tokens acquired")

    try:
        response = await acompletion(
            model=model,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
        )
        logger.debug("Received successful response")
        return response.model_dump_json(indent=2), response._hidden_params["response_cost"]
    except Exception:
        logger.exception(f"Communication error with {model}")
        raise


async def ask_llm_async_with_schema(
    model: str,
    sys_prompt: str,
    user_prompt: str,
    output_class: type[T],
    top_p: float = 1,
    temperature: float = 0.5,
) -> tuple[str | T, float]:
    """Ask the LLM asynchronously with schema.

    Args:
        model: The model to use.
        sys_prompt: The system prompt.
        user_prompt: The user prompt.
        output_class: The output class.
        top_p: The top p value.
        temperature: The temperature value.

    Returns:
        The response from the LLM and the cost of the request.
    """
    logger.info(f"Calling for {model} with schema")
    load_dotenv()

    if not supports_response_schema(model=model):
        msg = f"Model {model} does not support schemas, use the `ask_llm_async` function instead"
        logger.error(msg)
        raise ValueError(msg)

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt},
    ]
    await rate_limiter.async_acquire(token_counter(model, messages=messages))
    logger.info("Rate limit tokens acquired")

    try:
        response = await acompletion(
            model=model,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
            response_format=output_class,
        )
        logger.debug("Received successful response")
        content = response.choices[0].message.content
        return output_class.model_validate_json(content), response._hidden_params["response_cost"]
    except Exception:
        logger.exception(f"Communication error with {model}")
        raise
