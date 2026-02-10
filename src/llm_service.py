"""
LLM Service - Handles all interactions with the OpenAI API.

This is the single place where we talk to OpenAI.
If we ever switch to Anthropic or another provider,
we only need to change THIS file.
"""
from openai import OpenAI, APIError, RateLimitError
from config import settings
import logging
import time

logger = logging.getLogger(__name__)

class LLMService:
    """Wrapper around the OpenAI API with error handling and retries."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.max_tokens

    def generate(self, prompt: str, system_message: str = None,
                 temperature: float = 0.7, max_retries: int = 3) -> str:
        """
        Send a prompt to the LLM and return the response.

        Args:
            prompt: The user's message
            system_message: Optional instructions for the AI's behavior
            temperature: Creativity level (0=focused, 1=creative)
            max_retries: How many times to retry if the API fails

        Returns:
            The AI-generated text response
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        # Retry logic - APIs can temporarily fail due to rate limits,
        # network issues, or server overload. A professional service
        # handles this gracefully instead of crashing.
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=self.max_tokens,
                )
                return response.choices[0].message.content

            except RateLimitError:
                # We hit the rate limit - wait and try again
                wait_time = 2 ** attempt  # 1s, 2s, 4s (exponential backoff)
                logger.warning(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)

            except APIError as e:
                logger.error(f"OpenAI API error: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)

# Create a single instance to reuse across the application
llm_service = LLMService()

if __name__ == "__main__":
    logging.basicConfig(level=settings.log_level)
    reply = llm_service.generate("Say 'OK' in one word.")
    print(reply)

