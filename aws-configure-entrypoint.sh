#!/bin/bash

# Configurar AWS CLI se as variáveis estiverem definidas
if [ ! -z "$AWS_ACCESS_KEY_ID" ] && [ ! -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "Configurando AWS CLI..."
    aws configure set aws_access_key_id "${AWS_ACCESS_KEY_ID}"
    aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"
    aws configure set default.region "${AWS_DEFAULT_REGION:-us-east-1}"
    aws configure set default.output json
    
    echo "AWS CLI configurado com sucesso!"
    aws sts get-caller-identity 2>/dev/null || echo "Aviso: Não foi possível verificar credenciais AWS"
fi

# Executar comando passado
exec "$@"