import sqlite3
import subprocess
from pathlib import Path

output = Path("staticevolution.db")
output.unlink(missing_ok=True)
if any(Path("data").glob("*.metadata.json")):
    subprocess.run(
        ["sqlite-diffable", "load", str(output), "data", "--replace"],
        check=True,
    )
else:
    sqlite3.connect(output).close()
