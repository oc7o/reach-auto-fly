import os

from dotenv import load_dotenv

load_dotenv()

PERSON_RECOGNITION_ACCEPTANCE: float = float(
    os.environ.get("PERSON_RECOGNITION_ACCEPTANCE", 0.2)
)
