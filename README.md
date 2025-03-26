# Liquor Management System

This repository contains the backend and frontend code for the Liquor Management System, a comprehensive solution for managing liquor shops.

## System Architecture

The system is built using a microservices architecture with the following services:

- **Auth Service**: Handles authentication, authorization, and user management
- **Core Service**: Manages core entities like tenants and shops
- **Inventory Service**: Manages products, brands, stock, and suppliers
- **Sales Service**: Handles sales, returns, and cash management
- **Purchase Service**: Manages purchase orders and goods receipts
- **Accounting Service**: Handles accounting, journals, and ledgers
- **Reporting Service**: Generates reports and analytics

## Running with Docker Compose

The easiest way to run the system is using Docker Compose, which will start all the required services.

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### Steps to Run

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd LiquorManagement-including-inventory-management
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Check the status of the services:
   ```bash
   docker-compose ps
   ```

4. Access the services:
   - Auth Service: http://localhost:8001
   - Core Service: http://localhost:8002
   - Inventory Service: http://localhost:8003
   - Sales Service: http://localhost:8004
   - Purchase Service: http://localhost:8005
   - Accounting Service: http://localhost:8006
   - Reporting Service: http://localhost:8007

5. To stop the services:
   ```bash
   docker-compose down
   ```

## Running with Kubernetes

For production deployments, you can use Kubernetes to run the system.

### Prerequisites

- Kubernetes cluster (local or cloud-based)
- kubectl configured to connect to your cluster
- Docker (for building images)
- Docker registry (optional, for pushing images)

### Steps to Deploy

1. Navigate to the k8s directory:
   ```bash
   cd k8s
   ```

2. Configure the deployment:
   - Edit the ConfigMap and Secrets in `01-configmap.yaml` and `02-secrets.yaml` as needed
   - If using a private Docker registry, set the `DOCKER_REGISTRY` environment variable

3. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

4. Check the status of the deployment:
   ```bash
   kubectl get pods -n liquor-system
   ```

5. Access the services:
   - By default, the services are exposed as ClusterIP services
   - You can use port-forwarding to access them:
     ```bash
     kubectl port-forward service/auth-service 8001:8000 -n liquor-system
     ```
   - Or create Ingress resources to expose them externally

## Environment Variables

The following environment variables are used by the services:

- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `REDIS_URL`: Redis URL
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers

## Development

### Backend

The backend is built using Django and Django REST Framework. Each service is a separate Django project.

To run a service locally:

1. Navigate to the service directory:
   ```bash
   cd Liquor-backend/src/auth_service
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend

The frontend is built using React and TypeScript.

To run the frontend locally:

1. Navigate to the frontend directory:
   ```bash
   cd liquor-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## License

[Specify the license here]
