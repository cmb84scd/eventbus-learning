#!/usr/bin/env python3
"""Create the eventbus-learning stack."""

import aws_cdk as cdk
from decouple import config
from eventbus_learning.infrastructure.stack import EventbusLearningStack

app = cdk.App()
EventbusLearningStack(
    app,
    "eventbus-learning",
    env=cdk.Environment(
        account=config("AWS_ACCOUNT_ID"), region=config("AWS_REGION")
    ),
)

app.synth()
