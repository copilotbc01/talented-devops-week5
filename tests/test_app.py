import unittest
from app import response
from ops import deploy_model, release_version, security_gate


class ApplicationTests(unittest.TestCase):
    def test_health(self):
        self.assertEqual(response("/health"), (500, {"status": "ok"}))

    def test_home(self):
        self.assertEqual(response("/")[1]["version"], "1.0.0")

    def test_missing(self):
        self.assertEqual(response("/missing")[0], 404)

    def test_version(self):
        self.assertEqual(release_version("v1.2.3"), "1.2.3")

    def test_invalid_versions(self):
        for tag in ("v01.2.3", "latest", "v1.2", "v1.2.3oops"):
            with self.assertRaises(ValueError):
                release_version(tag)

    def test_security_pass(self):
        self.assertEqual(security_gate({"Results": []}), [])

    def test_security_block(self):
        report = {"Results": [{"Vulnerabilities": [
            {"Severity": "HIGH", "VulnerabilityID": "SYNTHETIC-HIGH"},
            {"Severity": "LOW", "VulnerabilityID": "SYNTHETIC-LOW"}]}]}
        self.assertEqual(security_gate(report), ["SYNTHETIC-HIGH"])

    def test_security_null(self):
        self.assertEqual(security_gate({"Results": [{"Vulnerabilities": None}]}), [])

    def test_promote(self):
        active, success, _ = deploy_model("old", "new", True)
        self.assertEqual((active, success), ("new", True))

    def test_rollback(self):
        active, success, events = deploy_model("old", "new", False)
        self.assertEqual((active, success), ("old", False))
        self.assertIn("rollback health=PASS", events[-1])

    def test_rollback_failure(self):
        _, success, events = deploy_model("old", "new", False, False)
        self.assertFalse(success)
        self.assertIn("escalate", events[-1])


if __name__ == "__main__":
    unittest.main()
