#!/bin/bash

echo "Creating mock env vars"

if [ -f .env ] ; then
    echo "env exists"
else
    echo "creating .env file.."
    cat > .env << EOF
BUILD_TARGET=dev
DEBUG=true
CI=true
SECRET_KEY=678d139c89654d93698029b9bf92fb21dd711c68800a7411ccf148cfa2b9cb29
EMAIL_VERIFICATION_SECRET=TE7zJ6OWEJo0t9Ux9jjnEkCbIq-loH9wWYVpvy9S3wE

DB_NAME=db
DB_USER=dev
DB_PASSWORD=pass
DB_HOST=localhost
DB_PORT=5432

ALLOWED_HOSTS=http://localhost,127.0.0.1
CORS_ALLOWED_HOSTS=http://localhost:3000,http://127.0.0.1:3000
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

ACCESS_TOKEN_EXPIRE_MINUTES=50000
REFRESH_TOKEN_EXPIRE_DAYS=5000000
JWT_ISSUER=auth-service
EOF

    echo "created env file at $(pwd) with vars: "
    cat .env
fi