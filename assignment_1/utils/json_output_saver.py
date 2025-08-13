import os
import json
from typing import Dict, Any
from utils.constants import OUTPUT_DIR, RESUME_OUTPUT_DIR

def save_output_to_file(
    data: Dict[str, Any], filename: str, subfolder: str = ""
) -> None:
    """Save dict to a JSON file under output/[subfolder]/filename."""
    folder_path = os.path.join(OUTPUT_DIR, subfolder)
    os.makedirs(folder_path, exist_ok=True)

    output_path = os.path.join(folder_path, filename)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"💾 Saved output to: {output_path}")
