# Hello GitOps

A GitOps demo repository showcasing continuous deployment of a FastAPI application to Kubernetes using FluxCD.

## Overview

This repository demonstrates:
- A simple FastAPI application containerized with Docker
- CI/CD pipeline using GitHub Actions (build, scan, deploy)
- GitOps-based deployment with FluxCD
- Automated image updates to Kubernetes manifests

## Quick Start (Dev/Prod)

| Environment | Flux path in `clusters/kind/flux-system/kustomization.yaml` | `APP_ENV` | Served page |
|-------------|--------------------------------------------------------------|-----------|-------------|
| Dev         | `../../../k8s/overlays/dev`                                  | `dev`     | `app/index.dev.html` |
| Prod        | `../../../k8s/overlays/prod`                                 | `prod`    | `app/index.prod.html` |

After changing the path, apply the change and run:

```bash
flux reconcile kustomization flux-system -n flux-system --with-source
```

## Repository Structure

```
├── app/                    # Application source code
│   ├── main.py             # FastAPI application
│   ├── index.html          # Fallback/default HTML page
│   ├── index.dev.html      # Development HTML page
│   ├── index.prod.html     # Production HTML page
│   ├── Dockerfile          # Container build instructions
│   └── requirements.txt    # Python dependencies
├── k8s/
│   ├── base/               # Base Kubernetes manifests
│   │   ├── deployment.yaml # Application deployment
│   │   ├── service.yaml    # NodePort service
│   │   └── kustomization.yaml
│   └── overlays/           # Environment-specific overlays
│       ├── dev/
│       │   ├── deployment-patch.yaml
│       │   └── kustomization.yaml
│       └── prod/
│           ├── deployment-patch.yaml
│           └── kustomization.yaml
├── clusters/
│   └── kind/
│       └── flux-system/    # FluxCD configuration for kind cluster
│           ├── gotk-components.yaml
│           ├── gotk-sync.yaml
│           ├── kustomization.yaml
│           └── image-automation.yaml  # Image update automation
└── .github/
    └── workflows/
        └── ci.yaml         # CI/CD pipeline
```

## Kustomize Configuration

This repository uses [Kustomize](https://kustomize.io/) to manage Kubernetes manifests. There are two `kustomization.yaml` files, each serving a different purpose:

### File Locations and Purposes

| File | Purpose |
|------|---------|
| `k8s/base/kustomization.yaml` | Defines the base application resources (deployment + service) |
| `clusters/kind/flux-system/kustomization.yaml` | Flux cluster configuration that includes GitOps toolkit components and references the base app |

### How It Works

1. **Base Layer** (`k8s/base/`) - Contains reusable, environment-agnostic manifests:
   ```yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   resources:
     - deployment.yaml
     - service.yaml
   ```

2. **Cluster Layer** (`clusters/kind/flux-system/`) - Cluster-specific configuration that composes resources:
   ```yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   resources:
     - gotk-components.yaml
     - gotk-sync.yaml
     - image-automation.yaml
     - ../../../k8s/overlays/dev  # References the dev overlay
   ```

## Environment Overlays (Dev vs Prod)

This repository now supports two visual variants of the app to simulate environments:

- `app/index.dev.html` (dev background/theme)
- `app/index.prod.html` (prod background/theme)

The FastAPI app chooses which file to serve based on the `APP_ENV` environment variable:

- `APP_ENV=dev` → serves `index.dev.html`
- `APP_ENV=prod` → serves `index.prod.html`
- Any other value (or missing) → serves `index.html` as fallback

### How overlays control the environment

Each overlay patches the Deployment and sets `APP_ENV`:

- `k8s/overlays/dev/deployment-patch.yaml` sets `APP_ENV=dev`
- `k8s/overlays/prod/deployment-patch.yaml` sets `APP_ENV=prod`

The cluster Kustomization currently points to the dev overlay:

```yaml
resources:
  - gotk-components.yaml
  - gotk-sync.yaml
  - image-automation.yaml
  - ../../../k8s/overlays/dev
```

### Switch between dev and prod

Edit `clusters/kind/flux-system/kustomization.yaml` and change:

- `../../../k8s/overlays/dev` → `../../../k8s/overlays/prod`

Then reconcile Flux:

```bash
flux reconcile kustomization flux-system -n flux-system --with-source
```

### Local testing without Kubernetes

You can test quickly by setting `APP_ENV` before running Uvicorn:

```bash
# Dev
APP_ENV=dev uvicorn main:app --host 0.0.0.0 --port 8080

# Prod
APP_ENV=prod uvicorn main:app --host 0.0.0.0 --port 8080
```

### Best Practices

- **Separation of concerns**: Keep base manifests generic and reusable; put environment-specific configs in cluster directories
- **DRY principle**: Define resources once in `base/`, reference them from multiple clusters/environments
- **Multi-cluster support**: Create separate directories under `clusters/` for each environment (e.g., `clusters/dev/`, `clusters/staging/`, `clusters/prod/`)
- **Overlays for customization**: Use Kustomize overlays to patch base resources with environment-specific values (replicas, resource limits, etc.)
- **Consistent naming**: Always name the file `kustomization.yaml` (not `kustomization.yml`) for tooling compatibility

### Extending for Multiple Environments

To add a new environment (e.g., production), create:

```
clusters/
├── kind/           # Development cluster
│   └── flux-system/
└── prod/           # Production cluster
    └── flux-system/
        ├── kustomization.yaml  # References k8s/base with prod overlays
        └── ...
```

## CI/CD Pipeline

The GitHub Actions workflow consists of three jobs:

1. **Unit Tests** - Runs `pytest` against the repository tests
2. **Build** - Builds the Docker image and pushes to GitHub Container Registry (ghcr.io)
3. **Scan** - Runs Trivy security scans on filesystem and container image

When code is pushed to `main`, the pipeline builds and scans a new image. Flux Image Automation then detects the new tag and updates `k8s/base/deployment.yaml` directly from the cluster-side controllers.

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

## Image Automation

This repository uses Flux Image Automation to automatically update the deployment manifest when new container images are pushed to the registry. CI only builds/scans/pushes images; Flux owns manifest updates.

### How It Works

Flux Image Automation consists of three components:

| Component | Purpose |
|-----------|---------|
| **ImageRepository** | Scans the container registry (`ghcr.io/rmiravalles/gitops-fastapi`) at regular intervals to discover available image tags |
| **ImagePolicy** | Defines the policy for selecting which image tag to use (in this repo: highest numeric CI run tag) |
| **ImageUpdateAutomation** | Commits the selected image tag to the Git repository when a new image is detected |

### Marker Comments

Flux identifies which lines to update using special marker comments in the deployment manifest:

```yaml
image: ghcr.io/rmiravalles/gitops-fastapi:1234 # {"$imagepolicy": "flux-system:gitops-fastapi"}
```

The marker `{"$imagepolicy": "flux-system:gitops-fastapi"}` tells Flux to update this line using the `gitops-fastapi` ImagePolicy in the `flux-system` namespace.

In this repository, `ImageUpdateAutomation` pushes directly to `main`, so Flux updates are applied in the same branch that the cluster is reconciling.

### Image Automation Commands

```bash
# Check if ImageRepository is scanning the registry
flux get images repository -n flux-system

# View which tag the ImagePolicy selected
flux get images policy -n flux-system

# Check ImageUpdateAutomation status
flux get images update -n flux-system

# Force image scan
flux reconcile image repository gitops-fastapi -n flux-system

# Force image update check
flux reconcile image update flux-system -n flux-system
```

### Configuration Files

The image automation is configured in:
- `clusters/kind/flux-system/image-automation.yaml` - Contains ImageRepository, ImagePolicy, and ImageUpdateAutomation resources
- `k8s/base/deployment.yaml` - Contains the marker comment for image updates

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

- An HTML page (not JSON), with styling/background determined by `APP_ENV` and overlay selection.

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