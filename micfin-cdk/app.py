#!/usr/bin/env python3

from aws_cdk import core

from micfin_cdk.micfin_cdk_stack import MicfinCdkStack


app = core.App()
MicfinCdkStack(app, "MicfinCdkStack")

app.synth()
