#!/bin/bash

# Configurar AWS CLI se as variáveis estiverem definidas
echo "Configurando AWS CLI..."
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set default.region "$AWS_DEFAULT_REGION"
echo "AWS CLI configurado com sucesso!"
aws sts get-caller-identity 2>/dev/null || echo "Aviso: Não foi possível verificar credenciais AWS"

# Executar comando passado
exec "$@"