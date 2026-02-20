# Deploying application with GitOps

This repository demonstrates how to deploy a simple Python application using GitOps principles with FluxCD. The application is built and pushed to GitHub Container Registry, and then deployed to a Kubernetes cluster using FluxCD.

## FluxCD Bootstrap

To bootstrap FluxCD in your cluster, you can use the following command:

```bash
flux bootstrap github \
  --owner=your-github-username \
  --repository=your-repository-name \
  --branch=main \
  --path= your-path \
  --personal
```

This command will set up FluxCD in your Kubernetes cluster and connect it to the specified GitHub repository. Make sure to replace the `--owner`, `--repository`, `--branch`, and `--path` values with your own information.