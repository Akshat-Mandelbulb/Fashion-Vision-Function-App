import sys
from pathlib import Path

# Add src directory to Python path to make it the root module
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from app import app

__all__ = ["app"]
