import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE = "staticevolution.db"


class LaunchCommandTests(unittest.TestCase):
    def test_image_owns_single_immutable_database_launch(self):
        docker_cmd = next(
            line
            for line in (ROOT / "Dockerfile").read_text().splitlines()
            if line.startswith("CMD ")
        )
        railway_deploy = json.loads((ROOT / "railway.json").read_text())["deploy"]

        self.assertIn(f"--immutable {DATABASE}", docker_cmd)
        self.assertIn("--secret ${DATASETTE_SECRET}", docker_cmd)
        self.assertEqual(docker_cmd.count(DATABASE), 1)
        self.assertNotIn("startCommand", railway_deploy)

    def test_builder_uses_existing_canonical_snapshot_directory(self):
        builder = (ROOT / "build_database.py").read_text()

        self.assertIn('Path("data")', builder)
        self.assertNotIn('Path("staticevolution")', builder)


if __name__ == "__main__":
    unittest.main()
