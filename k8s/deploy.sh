#!/bin/bash

# Liquor Management System Kubernetes Deployment Script

# Configuration
DOCKER_REGISTRY=${DOCKER_REGISTRY:-"localhost:5000"}
NAMESPACE="liquor-system"
BUILD_IMAGES=${BUILD_IMAGES:-"true"}
PUSH_IMAGES=${PUSH_IMAGES:-"false"}
DEPLOY_K8S=${DEPLOY_K8S:-"true"}

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Services to deploy
SERVICES=(
  "auth_service"
  "core_service"
  "inventory_service"
  "sales_service"
  "purchase_service"
  "accounting_service"
  "reporting_service"
)

# Function to print colored messages
print_message() {
  local color=$1
  local message=$2
  echo -e "${color}${message}${NC}"
}

# Function to check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
  print_message "$YELLOW" "Checking prerequisites..."
  
  if ! command_exists docker; then
    print_message "$RED" "Docker is not installed. Please install Docker and try again."
    exit 1
  fi
  
  if ! command_exists kubectl; then
    print_message "$RED" "kubectl is not installed. Please install kubectl and try again."
    exit 1
  fi
  
  if [ "$DEPLOY_K8S" = "true" ]; then
    if ! kubectl cluster-info &>/dev/null; then
      print_message "$RED" "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
      exit 1
    fi
  fi
  
  print_message "$GREEN" "Prerequisites check passed."
}

# Build Docker images
build_images() {
  if [ "$BUILD_IMAGES" != "true" ]; then
    print_message "$YELLOW" "Skipping image build."
    return
  fi
  
  print_message "$YELLOW" "Building Docker images..."
  
  for service in "${SERVICES[@]}"; do
    print_message "$YELLOW" "Building $service..."
    docker build -t "${DOCKER_REGISTRY}/liquor-backend/${service}:latest" -f "../Liquor-backend/src/${service}/Dockerfile" "../Liquor-backend"
    
    if [ $? -ne 0 ]; then
      print_message "$RED" "Failed to build $service."
      exit 1
    fi
    
    print_message "$GREEN" "Successfully built $service."
  done
}

# Push Docker images to registry
push_images() {
  if [ "$PUSH_IMAGES" != "true" ]; then
    print_message "$YELLOW" "Skipping image push."
    return
  fi
  
  print_message "$YELLOW" "Pushing Docker images to registry..."
  
  for service in "${SERVICES[@]}"; do
    print_message "$YELLOW" "Pushing $service..."
    docker push "${DOCKER_REGISTRY}/liquor-backend/${service}:latest"
    
    if [ $? -ne 0 ]; then
      print_message "$RED" "Failed to push $service."
      exit 1
    fi
    
    print_message "$GREEN" "Successfully pushed $service."
  done
}

# Deploy to Kubernetes
deploy_to_k8s() {
  if [ "$DEPLOY_K8S" != "true" ]; then
    print_message "$YELLOW" "Skipping Kubernetes deployment."
    return
  fi
  
  print_message "$YELLOW" "Deploying to Kubernetes..."
  
  # Create namespace if it doesn't exist
  kubectl apply -f 00-namespace.yaml
  
  # Apply ConfigMap and Secrets
  kubectl apply -f 01-configmap.yaml
  kubectl apply -f 02-secrets.yaml
  
  # Deploy infrastructure services
  print_message "$YELLOW" "Deploying infrastructure services..."
  kubectl apply -f 03-postgres.yaml
  kubectl apply -f 04-redis.yaml
  kubectl apply -f 05-kafka.yaml
  
  # Wait for infrastructure services to be ready
  print_message "$YELLOW" "Waiting for infrastructure services to be ready..."
  kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s -n $NAMESPACE
  kubectl wait --for=condition=ready pod -l app=redis --timeout=300s -n $NAMESPACE
  kubectl wait --for=condition=ready pod -l app=zookeeper --timeout=300s -n $NAMESPACE
  kubectl wait --for=condition=ready pod -l app=kafka --timeout=300s -n $NAMESPACE
  
  # Deploy application services
  print_message "$YELLOW" "Deploying application services..."
  
  # Replace ${DOCKER_REGISTRY} placeholder in YAML files
  for file in 06-*.yaml; do
    sed "s|\${DOCKER_REGISTRY}|${DOCKER_REGISTRY}|g" "$file" | kubectl apply -f -
  done
  
  print_message "$GREEN" "Deployment completed successfully."
}

# Main execution
main() {
  print_message "$YELLOW" "Starting Liquor Management System deployment..."
  
  check_prerequisites
  build_images
  push_images
  deploy_to_k8s
  
  print_message "$GREEN" "Deployment process completed."
}

# Run the main function
main
