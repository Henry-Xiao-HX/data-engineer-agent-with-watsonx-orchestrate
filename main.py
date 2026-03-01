#!/usr/bin/env python3
"""
Data Engineer Agent with watsonx Orchestrate
---------------------------------------------
Helper script to deploy or tear down the Data Intelligence MCP toolkit
and the data-engineer-agent into a watsonx Orchestrate environment.

Usage:
    uv run main.py deploy    # import toolkit + agent
    uv run main.py teardown  # remove agent + toolkit
    uv run main.py status    # list toolkit and agent
"""

import subprocess
import sys


TOOLKIT_FILE = "toolkit-wxdi.yaml"
AGENT_FILE = "agent-data-engineer.yaml"
TOOLKIT_NAME = "wxdi-mcp-toolkit"
AGENT_NAME = "data-engineer-agent"


def run(cmd: list[str]) -> int:
    """Run an orchestrate CLI command and return the exit code."""
    full_cmd = ["uv", "run", "orchestrate"] + cmd
    print(f"\n$ {' '.join(full_cmd)}")
    result = subprocess.run(full_cmd)
    return result.returncode


def deploy():
    print("=== Deploying Data Engineer Agent ===")

    print("\n[1/2] Importing MCP toolkit...")
    rc = run(["toolkits", "import", "--file", TOOLKIT_FILE])
    if rc != 0:
        print(f"  ⚠️  Toolkit import returned exit code {rc}. "
              "It may already exist — continuing.")

    print("\n[2/2] Importing agent...")
    rc = run(["agents", "import", "--file", AGENT_FILE])
    if rc != 0:
        print(f"  ⚠️  Agent import returned exit code {rc}. "
              "It may already exist — continuing.")

    print("\n✅ Deployment complete. Run `uv run main.py status` to verify.")


def teardown():
    print("=== Tearing down Data Engineer Agent ===")

    print("\n[1/2] Removing agent...")
    run(["agents", "remove", "--name", AGENT_NAME])

    print("\n[2/2] Removing toolkit...")
    run(["toolkits", "remove", "--name", TOOLKIT_NAME])

    print("\n✅ Teardown complete.")


def status():
    print("=== Toolkit Status ===")
    run(["toolkits", "list"])

    print("\n=== Agent Status ===")
    run(["agents", "list"])


def main():
    commands = {
        "deploy": deploy,
        "teardown": teardown,
        "status": status,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(__doc__)
        print(f"Available commands: {', '.join(commands)}")
        sys.exit(1)

    commands[sys.argv[1]]()


if __name__ == "__main__":
    main()

# Made with Bob
