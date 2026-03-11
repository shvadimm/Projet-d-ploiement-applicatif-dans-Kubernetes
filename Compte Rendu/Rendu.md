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


### Installation des StorageClass

```
-- Prérequis : Installation du driver CSI pour NFS -- 
helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
helm install csi-driver-nfs csi-driver-nfs/csi-driver-nfs --namespace nfs --create-namespace --version v4.10.0

kubectl apply -f storage-class-nfs.yml

```