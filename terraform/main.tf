# Criando o bucket s3
resource "aws_s3_bucket" "mercadolibre_scrapper_data" {
  bucket = var.bucket_name
  force_destroy = true
  tags = {
    Name = "Bucket para salvar os arquivos .csv"
    Environment = "Scripts"
  }
}

# Criando a role para a lambda function
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

data "aws_ecr_repository" "mercadolibre_scrapper_repository" {
  name = "mercadolibre-scrapper-repository"
}

# Obtendo o digest da imagem
data "aws_ecr_image" "mercadolibre_scrapper_image" {
  repository_name = data.aws_ecr_repository.mercadolibre_scrapper_repository.name
  image_tag = var.image_tag
}

# Criando uma aws policy para a lambda ter permissão de acessar o s3
resource "aws_iam_policy" "lambda_s3_policy" {
  name = "lambda-s3-putobject"
  description = "Allow Lambda to put objects in S3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [

      {
        Effect = "Allow"
        Action = [
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::mercadolibre-scrapper-data/*"
      }
    ]
  })
}

# Criando a policy para a lambda function
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_s3_policy.arn
}

# Criando a lambda function
resource "aws_lambda_function" "mercadolibre_scrapper_lambda" {
  function_name = var.lambda_function_name
  package_type  = "Image"
  role          = aws_iam_role.lambda_exec_role.arn

  image_uri = "${data.aws_ecr_repository.mercadolibre_scrapper_repository.repository_url}@${data.aws_ecr_image.mercadolibre_scrapper_image.image_digest}"

  timeout     = 900
  memory_size = 3008

  environment {
    variables = {
      ECR_REPO_URL = data.aws_ecr_repository.mercadolibre_scrapper_repository.repository_url
    }
  }
}