resource "aws_ecr_repository" "mercadolibre_scrapper_repository" {
  name = var.ecr_repository_name
    image_scanning_configuration {
        scan_on_push = true
  }
}
resource "null_resource" "docker_push" {
  # triggers = {
  #   dockerfile_changes = filemd5("${path.root}/../Dockerfile.lambda")
  #   script_changes     = filemd5("${path.root}/../scripts/lambda_scrapper_mercadolibre.py")
  # }

  provisioner "local-exec" {
    command = <<-EOT
      # Login no ECR
      aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${aws_ecr_repository.mercadolibre_scrapper_repository.repository_url}
      
      # Build da imagem
      docker build -f ${path.root}/../Dockerfile.lambda -t mercadolibre-scrapper ${path.root}/../
      
      # Tag da imagem
      docker tag mercadolibre-scrapper:latest ${aws_ecr_repository.mercadolibre_scrapper_repository.repository_url}:latest
      
      # Push da imagem
      docker push ${aws_ecr_repository.mercadolibre_scrapper_repository.repository_url}:latest
    EOT
  }

  depends_on = [aws_ecr_repository.mercadolibre_scrapper_repository]
}
output "ecr_repo_url" {
  value = aws_ecr_repository.mercadolibre_scrapper_repository.repository_url
}

output "ecr_repo_arn" {
  value = aws_ecr_repository.mercadolibre_scrapper_repository.arn
}