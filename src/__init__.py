"""
Initialize src package
"""

import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

__version__ = "1.0.0"
__author__ = "Data Engineering"
