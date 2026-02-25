import logging
from typing import Iterable, Tuple

from openai import AsyncAzureOpenAI
from openai.types.chat import ChatCompletionMessageParam

from config import Config
from shared.utils.timer import time_execution

logger = logging.getLogger(__name__)


class AzureOpenAIService:
    _instance = None
    client: AsyncAzureOpenAI

    def __new__(cls):
        if not Config.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT is not set in configuration")

        if not Config.AZURE_OPENAI_KEY:
            raise ValueError("AZURE_OPENAI_KEY is not set in configuration")

        if cls._instance is None:
            cls._instance = super(AzureOpenAIService, cls).__new__(cls)
            cls._instance.client = AsyncAzureOpenAI(
                azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                api_key=Config.AZURE_OPENAI_KEY,
                api_version=Config.AZURE_OPENAI_API_VERSION,
                timeout=120.0,  # 2 minute timeout
                max_retries=3,  # Retry up to 3 times on transient failures
            )
            logger.info("AzureOpenAIService initialized successfully.")
        else:
            logger.info("AzureOpenAIService instance already exists.")
        return cls._instance

    def __init__(self):
        pass

    @time_execution
    async def chat_completion_text(
        self, messages: Iterable[ChatCompletionMessageParam], max_tokens: int = 2000
    ) -> Tuple[str, int]:
        if not self.client:
            raise ValueError("Azure OpenAI client not initialized")
        if not Config.AZURE_OPENAI_DEPLOYMENT_NAME:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME is not set in configuration")
        try:
            response = await self.client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
            )

            answer = response.choices[0].message.content or ""
            tokens_used = 0

            if response.usage is not None:
                tokens_used = response.usage.total_tokens

            logger.info(f"GPT-4 text completion Tokens Used: {tokens_used}")

            return answer, tokens_used
        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}", exc_info=True)
            raise Exception(f"Failed to generate response: {str(e)}")

    async def close(self):
        """Close Azure OpenAI client to prevent resource leaks"""
        try:
            if self.client:
                await self.client.close()
                logger.info("Azure OpenAI client closed")
        except Exception as e:
            logger.error(f"Error closing Azure OpenAI client: {str(e)}", exc_info=True)

    async def __aenter__(self):
        """Context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources"""
        await self.close()
