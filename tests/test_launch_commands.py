import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE = "staticevolution.db"


class LaunchCommandTests(unittest.TestCase):
    def test_database_is_registered_once_as_immutable(self):
        docker_cmd = next(
            line for line in (ROOT / "Dockerfile").read_text().splitlines()
            if line.startswith("CMD ")
        )
        railway_cmd = json.loads((ROOT / "railway.json").read_text())["deploy"][
            "startCommand"
        ]

        for name, command in (("Dockerfile", docker_cmd), ("railway.json", railway_cmd)):
            with self.subTest(name=name):
                self.assertIn(f"--immutable {DATABASE}", command)
                self.assertEqual(command.split().count(DATABASE), 1)


if __name__ == "__main__":
    unittest.main()
