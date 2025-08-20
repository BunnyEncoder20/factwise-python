# Helper util for JSON file persistance

import json
import os
from typing import Dict, Any

class FileDB:
    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump({}, f)

    def read(self) -> Dict[str, Any]:
        if not os.path.exists(self.path): return {}
        with open(self.path, 'r') as f:
            return json.load(f)

    def write(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)
