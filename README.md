# Face Recognition Application Deployment with CI/CD


A simple face recognition application that allows users to upload images and receive recognition results. The application consists of two components:
1. The backend API implemented in Python using FastAPI, which offers facial recognition capabilities.
2. The frontend built with Kotlin using Ktor, which provides a simple web interface to upload images and display the recognition results.



## Kubernetes
Below is the architecture diagram illustrating the deployment in Kubernetes:


```mermaid
graph 
subgraph Kubernetes Cluster
subgraph Namespace: jku-clc-ws24
A[Frontend Pod<br> 2 replicas] -- Exposes: 8081 --> B[Frontend Service<br>ClusterIP]
C[Backend Pod<br> 2 replicas] -- Exposes: 8000 --> D[Backend Service<br>LoadBalancer]
end
subgraph Namespace: jku-clc-ws24-dev
E[Frontend Pod<br>1 replica] -- Exposes: 8081 --> F[Frontend Service<br>ClusterIP]
G[Backend Pod<br>1 replica] -- Exposes: 8000 --> H[Backend Service<br>ClusterIP]
end
B -- Internal Traffic --> D
F -- Internal Traffic --> H
end
```

### Deployment Overview

#### Namespaces
Two namespaces are used for the deployment: `jku-clc-ws24` for production and `jku-clc-ws24-dev` for development. The production namespace is used for the final deployment, while the development namespace is used for testing purposes.


#### Frontend Deployment
The frontend component runs two replicas of the `andih82/jku-clc-ws24-frontend` Docker image. It exposes port `8081` and communicates with the backend service using the environment variables `API_IP` and `API_PORT`.
The two replicals allow a Rolling Update strategy to be used for deployments with no downtime.

In the development namespace, the frontend component runs only one replica, which is sufficient for testing purposes.

#### Backend Deployment
The backend component runs two replicas of the `andih82/jku-clc-ws24-backend` Docker image. It exposes port `8000` and is used by the frontend service to perform facial recognition.
The two replicals allow a Rolling Update strategy to be used for deployments with no downtime.

In the development namespace, the backend component runs only one replica, which is sufficient for testing purposes.


### Services

#### Frontend Service
The frontend service exposes the frontend application on port `8081` within the cluster. It uses a `ClusterIP` type.
For development, the frontend service is configured with a `ClusterIP` type.
We decided to use a ClusterIP, to avoid exposing the frontend to the public and for Demo purposes we can use port-forwarding to access the frontend.


#### Backend Service
The backend service exposes the backend application on port `8001` and is configured as a `LoadBalancer` with an internal load balancer.
For development, the backend service is configured with a `ClusterIP` type, there is only one replica running in the development namespace, so no need for a load balancer.

### How to Deploy initially

1. Apply the namespace configuration:
   ```sh
   kubectl apply -f namespace.yaml
   ```

2. Deploy the frontend:
   ```sh
   kubectl apply -f frontend-deployment.yaml
   ```

3. Deploy the backend:
   ```sh
   kubectl apply -f backend-deployment.yaml
   ```

4. Apply the services:
   ```sh
   kubectl apply -f frontend-service.yaml
   kubectl apply -f backend-service.yaml
   ```
5. Access the frontend service using port-forwarding:
   ```sh
   kubectl port-forward svc/frontend-service 8080:8081 -n jku-clc-ws24
   ```
6. Access the frontend in your browser at `http://localhost:8080/upload`.

### Notes
- Free autocluster has limited resources, so the production deployment is limited to two replicas. Usually the backend service would have more replicas to handle the load and resource heavy task.
- For the development deployment, only one replica is used for each component to save resources. Downtime is acceptable for development purposes.
- The deployment needs readiness and liveness probes to ensure the application is running correctly.
- The frontend can be exposed using an Ingress controller for production deployments.
- The deployment can be extended with a database to store recognition results.

## CI/CD Pipeline
The CI/CD pipeline is implemented using GitHub Actions. The pipeline consists of the following stages:
The backend and frontend repositories are configured with GitHub Actions to trigger the pipeline on push events with version tag. The pipeline builds the Docker images, pushes them to the Google Container Registry, and deploys them to the GKE cluster. The deployment is updated with the new image, ensuring the latest version is running in the cluster.


### Frontend CI/CD Pipeline
1. Build: Builds the Docker images for the frontend and backend components.
2. Push: Pushes the Docker images to the Google Container Registry.
3. Deploy: Deploys the images to the Google Kubernetes Engine (GKE) cluster.
4. Update: Updates the deployment (pods) with the new image
```mermaid
graph 
    Develop -->|push| A[GitHub Repository]
subgraph Repositories
A[Frontend Repository]
end
subgraph GitHub Actions
    subgraph Frontend [Frontend CI/CD,  triggered on push with version tag]
        A1[Build Docker Image] -->
        A2[Push Docker Image] -->
        A3[Deploy to GKE]
    end
end
A --> |triggers| A1

A2 --> |push| CR[Container Registry]
CR --> |use| A3  

A3 --> |set image| K8s[GKE Kubernetes Cluster]

K8s -->|Update| F[Frontend Deployment]

```
For development, the pipeline is triggered on push events to the `develop` branch. The pipeline builds the Docker images, pushes them to the Google Container Registry, and deploys them to the GKE cluster. The deployment is updated with the new image, ensuring the latest version is running in the cluster.

### Backend CI/CD Pipeline
Is configured in the same way as the frontend pipeline, but with different Docker images and deployment configurations.

### Notes
- The pipline should be extended with tests to ensure the application is working correctly before deployment.
- The pipeline can be extended with manual approval steps for production deployments.
- The versioning of the Docker images is done using the Git tag, which is automatically created when a new version is pushed to the repository.
- A rollback strategy should be implemented in case the deployment fails.
- Relase tasks could be added to the pipeline to notify users of new deployments.
