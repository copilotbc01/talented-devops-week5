"""Deterministic policy and deployment model; no real registry or deployment."""
import json
import re
import sys


def release_version(ref):
    pattern = r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    if not re.fullmatch(pattern, ref):
        raise ValueError("Expected stable release tag vMAJOR.MINOR.PATCH")
    return ref[1:]


def security_gate(report):
    findings = []
    for result in report.get("Results", []):
        for item in result.get("Vulnerabilities", []) or []:
            if item.get("Severity") in {"HIGH", "CRITICAL"}:
                findings.append(item["VulnerabilityID"])
    return findings


def deploy_model(stable, candidate, candidate_healthy, stable_healthy=True):
    events = [f"stable={stable}", f"deploy candidate={candidate}"]
    if candidate_healthy:
        events.append("health=PASS; promote candidate")
        return candidate, True, events
    events.append("health=FAIL; rollback to previous stable")
    if not stable_healthy:
        events.append("rollback health=FAIL; escalate incident")
        return stable, False, events
    events.append("rollback health=PASS; stable restored")
    return stable, False, events


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "gate":
        with open(sys.argv[2], encoding="utf-8") as stream:
            blocked = security_gate(json.load(stream))
        print("BLOCK: " + ", ".join(blocked) if blocked else "PASS: no HIGH/CRITICAL")
        sys.exit(1 if blocked else 0)
    for healthy in (True, False):
        _, success, events = deploy_model("sha256:stable-demo", "sha256:candidate-demo", healthy)
        print("SIMULATION ONLY - " + ("SUCCESS" if success else "FAILED RELEASE / ROLLBACK"))
        print("\n".join(events))
