# Face Recognition Application Deployment with CI/CD

We want to develop a cloud-based application consisting of two services:  
1. The backend API implemented in Python using FastAPI, which offers facial recognition capabilities.  
2. The frontend built with Kotlin using Ktor, which provides a simple web interface to upload images and display the recognition results.  

The focus of the project is on utilizing cloud computing tools like containerization and automated deployment pipelines.

## Technology Stack

- **Backend**: Python with FastAPI for face recognition  
- **Frontend**: Kotlin with Ktor for web interface  
- **Containerization**: Docker  
- **Orchestration**: Kubernetes   
- **CI/CD**: GitHub Actions  

## Tasks

1. **Containerization**: Create Docker images for the backend and frontend services.  
2. **CI/CD Pipeline**:  
   - Set up GitHub workflows to trigger builds on code changes.  
   - Automate image building and deployment to Kubernetes.  
3. **Kubernetes Orchestration**:  
   - Deploy and manage the containers using Kubernetes.  

## Demonstration

- **Deployment Workflow**:  
  - Triggered by code changes via GitHub Actions.  
  - New images are built, pushed to a container registry, and deployed to the Kubernetes cluster.  
- **Kubernetes Overview**:  
  - Showcase running pods, nodes, and container orchestration.  
- **CI/CD Showcase**:  
  - Highlight GitHub Actions workflow configuration and execution.  
- **Application Demo**:  
  - Upload an image through the frontend.  
  - Display face recognition results processed by the backend.  

## Team Members

- Tim Lohninger, K12141837  
- Andreas Hofstadler, K12224237  
- Anna Kurzecka, K11939589  
