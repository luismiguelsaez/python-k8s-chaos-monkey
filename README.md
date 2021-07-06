Python K8S chaos monkey
=======================

## Requirements

- We're going to use the official Kubernetes client to be able to interact with Kubernetes API server ( https://github.com/kubernetes-client/python )
- To be able to connect to the Kubernetes API, we will define a role with permissions over the pods running on every namespace
- Application code is based on examples and documentation from official repository ( https://github.com/kubernetes-client/python/tree/master/examples )

## Cluster setup

### Start minikube cluster
```
minikube start
```

### Setup
```
kubectl apply -f k8s/role.yaml
```


k run test -n chaos --serviceaccount=pod-controller --rm=true -it --image=python:3.9-alpine --restart=Never --command -- sh