# Kubernetes Deployment Manifests

Complete Kubernetes deployment for the TODO application with replication, auto-scaling, and database integration with MariaDB Galera.

## Files Overview

| File | Purpose |
|------|---------|
| `00-namespace.yaml` | Creates the `todos` namespace |
| `01-secret.yaml` | Stores sensitive data (passwords, secret keys) |
| `02-configmap.yaml` | Stores configuration (database host, port, etc.) |
| `03-deployment.yaml` | Main application deployment (3 replicas with rolling updates) |
| `04-service.yaml` | LoadBalancer service to expose the application |
| `05-hpa.yaml` | HorizontalPodAutoscaler for automatic scaling |

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Kubernetes Cluster              │
├─────────────────────────────────────────┤
│  namespace: todos                       │
│  ┌───────────────────────────────────┐  │
│  │ Deployment: todos-app (3 replicas)│  │
│  │ - Pod 1 (todos-app-xxx)           │  │
│  │ - Pod 2 (todos-app-yyy)           │  │
│  │ - Pod 3 (todos-app-zzz)           │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │ Service: todos-app-service        │  │
│  │ (LoadBalancer on port 80)         │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │ ConfigMap: todos-config           │  │
│  │ Secret: todos-secret              │  │
│  │ HPA: todos-app-hpa                │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
        │
        │ (connects to)
        ▼
┌─────────────────────────────────────────┐
│    MariaDB Galera (3 replicas)          │
│    Deployed in default namespace        │
└─────────────────────────────────────────┘
```

## Deployment Instructions

### 1. Deploy Application
```bash
cd k8s-manifests
chmod +x deploy.sh
./deploy.sh
```

### 2. Manual Deployment (if needed)
```bash
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-secret.yaml
kubectl apply -f 02-configmap.yaml
kubectl apply -f 03-deployment.yaml
kubectl apply -f 04-service.yaml
kubectl apply -f 05-hpa.yaml
```

## Monitoring & Troubleshooting

### Check Status
```bash
# All resources
kubectl get all -n todos

# Pods only
kubectl get pods -n todos -o wide

# Services
kubectl get svc -n todos

# HPA status
kubectl get hpa -n todos
```

### Watch Deployment Progress
```bash
kubectl get pods -n todos -w
```

### View Logs
```bash
# All pods
kubectl logs -n todos -l app=todos-app --tail=100 -f

# Specific pod
kubectl logs -n todos <pod-name>
```

### Detailed Pod Information
```bash
kubectl describe pod -n todos <pod-name>
```

### Check Events
```bash
kubectl get events -n todos --sort-by='.lastTimestamp'
```

## Environment Variables

The application receives configuration from:

### From ConfigMap (`todos-config`)
- `DATABASE_HOST`: mariadb-galera
- `DATABASE_PORT`: 3306
- `DATABASE_NAME`: tododb
- `DATABASE_USER`: todouser
- `FLASK_ENV`: production

### From Secret (`todos-secret`)
- `DATABASE_PASSWORD`: todopass
- `SECRET_KEY`: Flask session secret

### Constructed
- `DATABASE_URL`: Auto-constructed from individual variables

## High Availability Features

✅ **Replication**: 3 Pod replicas (configurable)  
✅ **Rolling Updates**: Zero-downtime deployments  
✅ **Pod Anti-Affinity**: Spreads pods across nodes  
✅ **Health Checks**: Liveness & Readiness probes  
✅ **Resource Limits**: Prevents resource exhaustion  
✅ **Auto-Scaling**: Scales based on CPU/Memory  
✅ **Session Affinity**: Routes client to same pod  

## Updating Configuration

### Change Secret Values
```bash
kubectl edit secret todos-secret -n todos
```

### Change ConfigMap Values
```bash
kubectl edit configmap todos-config -n todos
```

### Restart Pods After Config Changes
```bash
kubectl rollout restart deployment/todos-app -n todos
```

## Connecting to Database

The app connects to MariaDB Galera at:
```
mysql+pymysql://todouser:todopass@mariadb-galera:3306/tododb
```

MariaDB is in the `default` namespace, so the connection uses the DNS name `mariadb-galera` (Kubernetes DNS resolves cross-namespace).

## Cleanup

Remove all resources:
```bash
kubectl delete namespace todos
```

## Metrics & Observability

### Current Setup
- Deployment with health checks (liveness/readiness)
- Resource requests/limits
- HPA with CPU/Memory metrics

### Future Enhancements
- Prometheus metrics export
- Grafana dashboards
- Centralized logging (ELK/Loki)
- Distributed tracing (Jaeger)

## Notes

- Replace sensitive values in `01-secret.yaml` with production secrets
- Adjust resource requests/limits in `03-deployment.yaml` based on your cluster capacity
- Modify replica counts and HPA settings as needed
- Change `LoadBalancer` to `ClusterIP` or `NodePort` if LoadBalancer isn't available
