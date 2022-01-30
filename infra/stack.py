import aws_cdk as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct


class PipelineStack(cdk.Stack):
    """PipelineStack defines the CI/CD pipeline for this application"""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        repo: str,
        repo_branch: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CodePipeline(
            self,
            "Pipeline",
            pipeline_name="LimitsManagementPipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.git_hub(
                    repo,
                    repo_branch,
                    authentication=cdk.SecretValue.secrets_manager("github-token"),
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    # "pytest",
                     "cdk synth",
                ],
            ),
        )
