### Auto Create IAM Policy & Sync Policy

### Excel to Json 

### AWS Service Classification

[Infra]
- VPC : `ec2:*`
- EC2 : `ec2:*`
- ECS : `ecs:*`
- EKS : `eks:*`
- Lambda : `lambda:*`

[Network]
- ELB (ELB v2) : `elasticloadbalancing:*`
- CloudFront : `cloudfront:*`
- Route53 : `route53:*`

[Storage]
- ECR : `ecr:*`
- ElastiCache : `elasticache:*`
- RDS : `rds:*`
- S3 : `s3:*`

[Security]
- `IAM` : `iam:*`

[Resource]
- Resource Group : `resource-groups:*`
- Systems Manager : `ssm:*`

[Mornitoring]
- CloudWatch : `cloudwatch:*`

[Resource]
- SystemManager : `ssm:*`
- ResourceGroup : `resource-groups:*`
