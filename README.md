# Hello GitOps

A GitOps demo repository showcasing continuous deployment of a FastAPI application to Kubernetes using FluxCD.

## Overview

This repository demonstrates:
- A simple FastAPI application containerized with Docker
- CI/CD pipeline using GitHub Actions (build, scan, deploy)
- GitOps-based deployment with FluxCD
- Automated image updates to Kubernetes manifests

## Repository Structure

```
├── app/                    # Application source code
│   ├── main.py             # FastAPI application
│   ├── Dockerfile          # Container build instructions
│   └── requirements.txt    # Python dependencies
├── k8s/
│   └── base/               # Kubernetes manifests
│       ├── deployment.yaml # Application deployment
│       ├── service.yaml    # NodePort service
│       └── kustomization.yaml
├── clusters/
│   └── kind/
│       └── flux-system/    # FluxCD configuration for kind cluster
└── .github/
    └── workflows/
        └── ci.yaml         # CI/CD pipeline
```

## CI/CD Pipeline

The GitHub Actions workflow consists of three jobs:

1. **Build** - Builds the Docker image and pushes to GitHub Container Registry (ghcr.io)
2. **Scan** - Runs Trivy security scans on filesystem and container image
3. **Deploy** - Updates the Kubernetes deployment manifest with the new image tag

When code is pushed to `main`, the pipeline automatically builds a new image, scans it for vulnerabilities, and commits the updated image tag to `k8s/base/deployment.yaml`. FluxCD then detects this change and deploys it to the cluster.

## Prerequisites

- Kubernetes cluster (kind, minikube, or any K8s cluster)
- [FluxCD CLI](https://fluxcd.io/flux/installation/)
- GitHub personal access token with `repo` permissions

## Installing FluxCD

### 1. Install the Flux CLI

```bash
# macOS
brew install fluxcd/tap/flux

# Linux
curl -s https://fluxcd.io/install.sh | sudo bash

# Windows (Chocolatey)
choco install flux
```

### 2. Check Prerequisites

```bash
flux check --pre
```

### 3. Export GitHub Token

```bash
export GITHUB_TOKEN=<your-github-personal-access-token>
```

### 4. Bootstrap FluxCD

For a kind cluster:

```bash
flux bootstrap github \
  --owner=rmiravalles \
  --repository=hello-gitops \
  --branch=main \
  --path=clusters/kind \
  --personal
```

This command will:
- Install FluxCD components in the `flux-system` namespace
- Create a deploy key for the repository
- Configure Flux to sync from the `clusters/kind` directory

### 5. Verify Installation

```bash
# Check Flux components
flux check

# Watch for reconciliation
flux get kustomizations --watch
```

## Accessing the Application

Once deployed, access the FastAPI application:

```bash
# Get the NodePort
kubectl get svc fastapi

# For kind, forward the port
kubectl port-forward svc/fastapi 8080:80

# Access the application
curl http://localhost:8080
```

Expected response:
```json
{"message": "Hello from GitOps with Flux 🚀"}
```

## Useful Flux Commands

```bash
# Trigger manual reconciliation
flux reconcile kustomization flux-system

# View Flux logs
flux logs

# Suspend/resume reconciliation
flux suspend kustomization flux-system
flux resume kustomization flux-system

# Uninstall Flux
flux uninstall
```