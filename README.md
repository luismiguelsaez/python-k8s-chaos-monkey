Python K8S chaos monkey
=======================

## Requirements

- We're going to use the official Kubernetes client to be able to interact with Kubernetes API server ( https://github.com/kubernetes-client/python )
- To be able to connect to the Kubernetes API, we will define a role with permissions over the pods running on every namespace
- Application code is based on examples and documentation from official repository ( https://github.com/kubernetes-client/python/tree/master/examples )

## Cluster setup

### Start kind cluster
```
kind create cluster --name chaos-monkey
```

### Configure needed role and permissions
```
kubectl apply -f k8s/role.yaml
```

## Build application

### Build image
```
docker build -t chaos-monkey:latest .
```

### Load image into cluster
```
kind load docker-image chaos-monkey:latest --name chaos-monkey
docker exec -it chaos-monkey-control-plane crictl images
```

### Deploy applications
```
kubectl apply -f k8s/deployment-nginx.yaml
kubectl apply -f k8s/deployment-chaos.yaml
```
