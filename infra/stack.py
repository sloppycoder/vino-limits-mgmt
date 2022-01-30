from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as pipeline_actions
from aws_cdk import core
from chalice.cdk import Chalice


class ChaliceApp(core.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.chalice = Chalice(
            self,
            "LimitsManagementApp",
            source_dir="../app",
        )


class Pipeline(core.Stack):
    """PipelineStack defines the CI/CD pipeline for this application"""

    def __init__(
        self,
        scope: core.Construct,
        construct_id: str,
        repo_owner: str,
        repo_name: str,
        repo_branch: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sourceArtifact = codepipeline.Artifact()
        cloudAssemblyArtifact = codepipeline.Artifact()
        codepipeline.CdkPipeline(
            self,
            "LimitsManagementPipeline",
            cloudAssemblyArtifact,
            sourceAction=pipeline_actions.GitHubSourceAction(
                actionName="GitHub",
                output=sourceArtifact,
                oauthToken=core.SecretValue.secretsManager("github-token"),
                owner=repo_owner,
                repo=repo_name,
                branch=repo_branch,
            ),
            synthAction=codepipeline.SimpleSynthAction.standardNpmSynth(
                sourceArtifact,
                cloudAssemblyArtifact,
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "python -m pytest",
                    "cdk synth",
                ],
            ),
        )


class MyAppStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        Pipeline(scope, construct_id, **kwargs)
