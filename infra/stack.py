import aws_cdk as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from chalice.cdk import Chalice
from constructs import Construct


class ChaliceApp(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.dynamodb_table = self._create_ddb_table()
        self.chalice = Chalice(
            self,
            "ChaliceApp",
            source_dir="../app",
        )


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
                    "pytest",
                    "cdk synth",
                ],
            ),
        )
        ChaliceApp()
