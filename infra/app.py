#!/usr/bin/env python3

import json
from aws_cdk import core
from stack import PipelineStack


app = core.App()

with open("../app/.chalice/config.json") as config_file:
    config = json.load(config_file)
    app_name = config["vino-limits-mgmt"]

PipelineStack(
    app,
    app_name,
    stack_name=f"{app_name}-pipeline",
    repo="sloppycoder/vino-limits-mgmt",
    repo_branch="develop",
)

app.synth()
