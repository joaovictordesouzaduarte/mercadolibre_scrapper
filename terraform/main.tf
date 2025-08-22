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
# Criando a policy para a lambda function
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Criando a lambda function
resource "aws_lambda_function" "mercadolibre_scrapper_lambda" {
  function_name = var.lambda_function_name
  image_uri = "086997587178.dkr.ecr.us-east-2.amazonaws.com/mercadolibre-scrapper-repository:latest"
  package_type = "Image"
  role = aws_iam_role.lambda_exec_role.arn
  handler = "lambda_scrapper_mercadolibre.lambda_handler"
  timeout = 900
  memory_size = 2048
  environment {
    variables = {
      ECR_REPO_URL = "086997587178.dkr.ecr.us-east-2.amazonaws.com/mercadolibre-scrapper-repository"
    }
  }
}