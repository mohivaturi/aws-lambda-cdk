from constructs import Construct  # Corrected import
from aws_cdk import (
    App, Stack, Environment
)
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_ec2 as ec2

class AwsLambdaCdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a VPC in us-east-1 with private and public subnets
        vpc = ec2.Vpc(self, "MyVpc",
            max_azs=2,  # Use two Availability Zones
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT  # Private Subnet
                ),
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC  # Public Subnet
                )
            ]
        )

        # Create the Lambda function in the private subnet
        my_lambda = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="hello_world.lambda_handler",  # Ensure this matches the file structure
            code=_lambda.Code.from_asset("lambda"),  # The Lambda code directory
            vpc=vpc,  # Attach to VPC
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
        )


app = App()
AwsLambdaCdkStack(app, "AwsLambdaCdkStack", env=Environment(account="640168419430", region="us-east-1"))
app.synth()



