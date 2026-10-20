output "resources" {
  value = {
    bucket         = aws_s3_bucket.lab.id
    vpc            = aws_vpc.lab.id
    subnets        = aws_subnet.lab[*].id
    security_group = aws_security_group.lab.id
    instance       = aws_instance.symbolic.id
  }
}
