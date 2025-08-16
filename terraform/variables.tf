variable "aws_region" {
  type    = string
  description = "AWS region"
}
variable "ecr_repository_name" {
  type    = string
  description = "ECR repository name"
}
variable "ecr_repository_tag" {
  type    = string
  description = "ECR repository tag"
}
variable "lambda_function_name" {
  type    = string
  description = "Lambda function name"
}