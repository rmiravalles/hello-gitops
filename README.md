# Deploying application with GitOps

## FluxCD Bootstrap

To bootstrap FluxCD in your cluster, you can use the following command:

```bash
flux bootstrap github \
  --owner=rmiravalles \
  --repository=hello-gitops \
  --branch=main \
  --path=./clusters/kind \
  --personal
```

This command will set up FluxCD in your Kubernetes cluster and connect it to the specified GitHub repository. Make sure to replace the `--owner`, `--repository`, `--branch`, and `--path` values with your own information.