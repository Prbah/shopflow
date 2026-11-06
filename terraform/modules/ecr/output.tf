output "repository_urls" {
  description = "ECR repository URLs"
  value       = {
    for service, repo in aws_ecr_repository.this :
    service => repo.repository_url
  }
}