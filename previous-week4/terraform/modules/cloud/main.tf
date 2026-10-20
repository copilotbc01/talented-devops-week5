resource "aws_s3_bucket" "lab" {
  bucket = "${var.project}-iac"
  tags   = { Project = var.project }
}
resource "aws_vpc" "lab" {
  cidr_block = "10.44.0.0/16"
  tags       = { Name = "${var.project}-vpc" }
}
resource "aws_subnet" "lab" {
  count             = 2
  vpc_id            = aws_vpc.lab.id
  cidr_block        = cidrsubnet(aws_vpc.lab.cidr_block, 8, count.index + 1)
  availability_zone = count.index == 0 ? "us-east-1a" : "us-east-1b"
  tags              = { Name = "${var.project}-subnet-${count.index + 1}" }
}
resource "aws_security_group" "lab" {
  name        = "${var.project}-sg"
  description = "Local emulation only"
  vpc_id      = aws_vpc.lab.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.44.0.0/16"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.44.0.0/16"]
  }
}
resource "aws_instance" "symbolic" {
  ami                    = "ami-12345678"
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.lab[0].id
  vpc_security_group_ids = [aws_security_group.lab.id]
  tags                   = { Name = "${var.project}-symbolic" }
}
