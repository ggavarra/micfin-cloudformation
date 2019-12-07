from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    core,
    aws_autoscaling as autoscaling
)


class MicfinCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        # Create a cluster
        vpc = ec2.Vpc(
            self, "MicFinVpc",
            max_azs=2
        )

        cluster = ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )
        cluster.add_capacity("DefaultAutoScalingGroup",
                             instance_type=ec2.InstanceType("t2.micro"),
                             machine_image=ecs.EcsOptimizedAmi(),
                             update_type=autoscaling.UpdateType.REPLACING_UPDATE,
                             desired_capacity=1

                             )


        # Create Task Definition
        task_definition = ecs.Ec2TaskDefinition(
            self, "TaskDef")
        container = task_definition.add_container(
            "web",
            image=ecs.ContainerImage.from_registry("210525354699.dkr.ecr.ap-southeast-1.amazonaws.com/micfin-repo"),
            memory_limit_mib=512
        )
        port_mapping = ecs.PortMapping(
            container_port=80,
            host_port=8080,
            protocol=ecs.Protocol.TCP
        )
        container.add_port_mappings(port_mapping)


        # Create Service
        service = ecs.Ec2Service(
            self, "Service",
            cluster=cluster,
            task_definition=task_definition
        )

        # Create ALB
        # lb = elbv2.ApplicationLoadBalancer(
        #     self, "LB",
        #     vpc=vpc,
        #     internet_facing=True
        # )
        # listener = lb.add_listener(
        #     "PublicListener",
        #     port=80,
        #     open=True
        # )
        #
        # health_check = elbv2.HealthCheck(
        #     interval=core.Duration.seconds(60),
        #     path="/health",
        #     timeout=core.Duration.seconds(5)
        # )
        #
        # # Attach ALB to ECS Service
        # listener.add_targets(
        #     "ECS",
        #     port=80,
        #     targets=[service],
        #     health_check=health_check,
        # )
        #
        # core.CfnOutput(
        #     self, "LoadBalancerDNS",
        #     value=lb.load_balancer_dns_name
        # )


