import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SLOPE_COLLECTOR_URL = os.environ["SLOPE_COLLECTOR_URL"]

O_MEET_PROTECTION_WORD = os.environ["O_MEET_PROTECTION_WORD"]
R_MEET_PROTECTION_WORD = os.environ["R_MEET_PROTECTION_WORD"]
MEET_PROTECTION_WORD = os.environ["MEET_PROTECTION_WORD"]
