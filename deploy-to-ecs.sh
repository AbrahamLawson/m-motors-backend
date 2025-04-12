#!/bin/bash

# Configuration - À REMPLIR
AWS_REGION="eu-west-3"  # Par exemple: Paris
APP_NAME="m-motors-backend"

echo "🚀 Étape 1: Connexion à AWS ECR"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com

echo "📦 Étape 2: Création du registre ECR"
aws ecr create-repository --repository-name $APP_NAME --region $AWS_REGION

# Récupère l'URI du registre
ECR_REGISTRY=$(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com
ECR_REPOSITORY=$ECR_REGISTRY/$APP_NAME

echo "🏗️ Étape 3: Construction de l'image Docker"
docker build -t $APP_NAME .

echo "🏷️ Étape 4: Tag de l'image"
docker tag $APP_NAME:latest $ECR_REPOSITORY:latest

echo "⬆️ Étape 5: Push de l'image vers ECR"
docker push $ECR_REPOSITORY:latest

echo "✅ Déploiement terminé!"
echo "URL de votre image: $ECR_REPOSITORY:latest"
echo "Utilisez cette URL dans la console AWS ECS pour créer votre service."
