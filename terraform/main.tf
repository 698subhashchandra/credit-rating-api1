resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "main_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone = "us-east-1a"
}

resource "aws_internet_gateway" "main_gw" {
  vpc_id = aws_vpc.main_vpc.id
}

resource "aws_route_table" "main_route_table" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_gw.id
  }
}

resource "aws_route_table_association" "main_rt_assoc" {
  subnet_id      = aws_subnet.main_subnet.id
  route_table_id = aws_route_table.main_route_table.id
}

resource "aws_security_group" "ubuntu_sg" {
  name_prefix = "ubuntu_sg_"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Replace with your IP for better security
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ubuntu_instance" {
  ami           = "ami-0c55b159cbfafe1f0" # Ubuntu 22.04 LTS in us-east-1 (update if necessary)
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.main_subnet.id
  security_groups = [aws_security_group.ubuntu_sg.name]

  key_name = aws_key_pair.main_key.key_name

  user_data = <<-EOF
              #!/bin/bash
              echo "Everything is running good"
              EOF

  tags = {
    Name = "UbuntuInstance"
  }
}

resource "aws_key_pair" "main_key" {
  key_name   = "main-key"
  public_key = file("~/.ssh/id_rsa.pub") # Ensure this file exists
}
