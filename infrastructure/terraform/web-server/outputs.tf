# Outputs do template de servidor web

output "vpc_id" {
  description = "ID da VPC"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID da subnet pública"
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "ID do security group"
  value       = aws_security_group.web.id
}

output "instance_id" {
  description = "ID da instância EC2"
  value       = aws_instance.web.id
}

output "instance_private_ip" {
  description = "IP privado da instância"
  value       = aws_instance.web.private_ip
}

output "instance_public_ip" {
  description = "IP público da instância"
  value       = aws_eip.web.public_ip
}

output "instance_dns" {
  description = "DNS público da instância"
  value       = aws_eip.web.public_dns
}

output "ssh_command" {
  description = "Comando SSH para conectar"
  value       = "ssh -i ${var.project_name}-key.pem ubuntu@${aws_eip.web.public_ip}"
}
