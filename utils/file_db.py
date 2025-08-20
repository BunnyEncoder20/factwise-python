# Helper util for JSON file persistance

import json
import os
from typing import Dict, Any

class FileDB:
    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, 'w') as file:
                json.dump({}, file)

    def read(self) -> Dict[str, Any]:
        # if not os.path.exists(self.path): return {}
        with open(self.path, 'r') as file:
            return json.load(file)

    def write(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as file:
            json.dump(data, file, indent=4)
