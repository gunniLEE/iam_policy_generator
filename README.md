# iam_policy_generator

### Auto Create IAM Policy

### Excel to Json

### AWS Service Classification
[Infra]
- VPC : `ec2:*`
- EC2 : `ec2:*`
- ECS : `ecs:*`
- EKS : `eks:*`

[Network]
- ELB (ELB v2) : `elasticloadbalancing:*`
- CloudFront : `cloudfront:*`
- Route53 : `route53:*`

[Storage]
- EBS : `ec2:*Volume*`
- ECR : `ecr:*`
- ElastiCache : `elasticache:*`
- RDS : `rds:*`
- S3 : `s3:*`

[Security]
- `IAM` : `iam:*`

[Resource]
- Resource Group : `resource-groups:*`
- Systems Manager : `ssm:*`
