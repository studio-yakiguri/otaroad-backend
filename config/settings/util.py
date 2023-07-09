import json
from pathlib import Path
from typing import Dict

# Common path settings
BASEDIR = Path(__file__).resolve().parent.parent.parent


# Get Key from /secure directory
def get_key_data(dir: str) -> dict:
    try:
        json_file = open(dir, 'r')
        data: Dict = dict(json.loads(json_file.read()))
        json_file.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"Not Found {dir} from /.secure directory")
    return data
