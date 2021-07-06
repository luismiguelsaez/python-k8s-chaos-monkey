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

## Deploy applications
We're going to create an `victim` deployment ( nginx ) and a `chaos` deployment
```
kubectl apply -f k8s/deployment-nginx.yaml
kubectl apply -f k8s/deployment-chaos.yaml
```

## Test
### Killing containers
Once deployed, we can see the pods randomly being killed by the application
```
kubectl get pods -n nginx
```
### Attacked service
We can launch requests against `nginx` service to see if it's still working
```
kubectl run test -n nginx --rm=true -it --image=alpine:3.12 --restart=Never --command -- sh
/ # wget -q http://nginx.nginx.svc -O-
```
### Prometheus metrics
Get prometheus killed containers metric through configured service
```
kubectl run test -n chaos --rm=true -it --image=alpine:3.12 --restart=Never --command -- sh
/ # wget chaos-monkey:8080 -q -O- | grep container_killed_total
# HELP container_killed_total Killed containers count
# TYPE container_killed_total counter
container_killed_total 28.0
```
