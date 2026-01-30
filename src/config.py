import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Azure Open Ai Configuration
    AZURE_OPENAI_ENDPOINT: Optional[str] = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY: Optional[str] = os.environ.get("AZURE_OPENAI_KEY")
    AZURE_OPENAI_API_VERSION: Optional[str] = os.environ.get("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_DEPLOYMENT_NAME: Optional[str] = os.environ.get(
        "AZURE_OPENAI_DEPLOYMENT_NAME"
    )

    # Azure Storage Configuration
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = os.environ.get(
        "AZURE_STORAGE_CONNECTION_STRING"
    )
    AZURE_STORAGE_ACCOUNT_NAME: Optional[str] = os.environ.get(
        "AZURE_STORAGE_ACCOUNT_NAME"
    )
    AZURE_STORAGE_ACCOUNT_KEY: Optional[str] = os.environ.get(
        "AZURE_STORAGE_ACCOUNT_KEY"
    )
