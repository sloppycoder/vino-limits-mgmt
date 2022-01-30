#!/usr/bin/env python3

import json

from aws_cdk import core
from stack import ChaliceApp, MyAppStack

app = core.App()
ChaliceApp(app, "limits-mgmt")

with open("app/.chalice/config.json") as config_file:
    config = json.load(config_file)
    app_name = config["app_name"]

MyAppStack(
    app,
    app_name,
    stack_name=f"{app_name}-pipeline",
    repo_owner="sloppycoder",
    repo_name="vino-limits-mgmt",
    repo_branch="develop",
)

app.synth()
