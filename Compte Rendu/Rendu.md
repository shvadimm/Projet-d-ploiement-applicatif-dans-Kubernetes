# Projet déploiement applicatif dans Kubernetes

## Déploiement dans le cluster
### Installation du Cluster

#### La mise en place de petit cluster kubernetes

`kind create cluster --config cluster-config.yml`

#### Installer loadbalancer MetalLB via Helm

```
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.15.3/config/manifests/metallb-native.yaml
```

#### Installer IngressController Traefik via helm

```
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik


```


# START HERE

# Create cluster
kind create cluster --config cluster-config.yml


# Create namespace, secrets & configmap
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-secret.yaml
kubectl apply -f 02-configmap.yaml

# mariadb-galera
## create a storageclass for the mariadb-galera
kubectl apply -f storageclass-mariadb.yaml

## create the mariadb-galera with helm
helm install my-release oci://registry-1.docker.io/bitnamicharts/mariadb-galera --namespace todos --create-namespace  -f mariadb-galera-values.yaml

# deploy the app
kubectl apply -f 03-deployment.yaml

# install traefik
helm install traefik traefik/traefik

## create clusterip for the ingress route
kubectl apply -f 04-service.yaml

# create the ingress
kubectl apply -f ingress/ingress.yaml


# port forward (les deux commandes font pareil)
kubectl port-forward svc/traefik 8000:80

ou

kubectl port-forward deployment/traefik 8000:8000


------

# Déploiement continu avec Flagger
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus -n monitoring --create-namespace

kubectl create namespace traefik

helm repo add flagger https://flagger.app
helm install flagger flagger/flagger \
  --namespace traefik \
  --set prometheus.url=http://prometheus-server.monitoring.svc.cluster.local \
  --set meshProvider=traefik

