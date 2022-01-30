#!/usr/bin/env python3

import json

import aws_cdk as cdk
from stack import PipelineStack

app = cdk.App()

with open("app/.chalice/config.json") as config_file:
    config = json.load(config_file)
    app_name = config["app_name"]

PipelineStack(
    app,
    app_name,
    stack_name=f"{app_name}-pipeline",
    repo="sloppycoder/vino-limits-mgmt",
    repo_branch="develop",
)

app.synth()
