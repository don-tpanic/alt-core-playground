"""LLM caller module."""

import asyncio
import logging
import time

from dotenv import load_dotenv
from litellm import acompletion, completion, token_counter


def get_num_tokens(model: str, messages: list[dict]) -> int:
    """Get the number of tokens in the system and user prompts.

    Args:
        model: The model to use.
        messages: The messages to count the tokens of.

    Returns:
        The number of tokens in the system and user prompts.
    """
    num_tokens = token_counter(
        model,
        messages=messages,
    )
    return num_tokens


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
        self.lock: asyncio.Lock = asyncio.Lock()

    async def acquire(self, tokens: int) -> None:
        """Acquire the tokens.

        Args:
            tokens: The number of tokens to acquire.
        """
        while True:
            async with self.lock:
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
                    return

            # If not enough tokens, wait a bit before checking again
            await asyncio.sleep(1)


rate_limiter = MinuteRateLimiter(tokens_per_minute=100000)


def ask_llm(
    model: str, sys_prompt: str, user_prompt: str, top_p: float = 1, temperature: float = 0.5
) -> tuple[str, float]:
    """Ask the LLM.

    Args:
        model: The model to use.
        sys_prompt: The system prompt.
        user_prompt: The user prompt.
        top_p: The top p value.
        temperature: The temperature value.

    Returns:
        The response from the API and the cost of the request.
    """
    logging.info(f"[ask_llm]: Calling for {model}")
    load_dotenv()

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Minimal error handling for now
    try:
        response = completion(
            model=model,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
        )

    except Exception as e:
        logging.error(f"An error occurred while attempting to communicate with {model}: {e}")
        raise e

    return response.model_dump_json(indent=2), response._hidden_params["response_cost"]


async def ask_llm_async(
    model: str, sys_prompt: str, user_prompt: str, top_p: float = 1, temperature: float = 0.5
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
    logging.info(f"[ask_llm_async]: Calling for {model}")
    load_dotenv()

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt},
    ]
    await rate_limiter.acquire(get_num_tokens(model, messages))

    # Minimal error handling for now
    try:
        response = await acompletion(
            model=model,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
        )

    except Exception as e:
        logging.error(f"An error occurred while attempting to communicate with {model}: {e}")
        raise e

    return response.model_dump_json(indent=2), response._hidden_params["response_cost"]
