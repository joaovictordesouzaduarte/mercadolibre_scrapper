variable "aws_region" {
  type    = string
  description = "AWS region"
}
variable "bucket_name" {
  type    = string
  description = "Bucket name"
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
variable "image_tag" {
  type    = string
  description = "Image tag"
  default = "latest"
}