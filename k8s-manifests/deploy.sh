#!/bin/bash
# Deploy entire application to Kubernetes cluster

set -e

echo "🚀 Deploying Application to Kubernetes..."
echo ""

# Apply manifests in order
echo "📦 Creating namespace..."
kubectl apply -f 00-namespace.yaml

echo "🔐 Creating secrets..."
kubectl apply -f 01-secret.yaml

echo "⚙️  Creating ConfigMap..."
kubectl apply -f 02-configmap.yaml

echo "🗄️  Creating MariaDB Galera cluster..."
kubectl apply -f 06-mariadb-galera.yaml

echo "⏳ Waiting for MariaDB Galera to be ready..."
kubectl rollout status statefulset/mariadb-galera -n todos --timeout=300s

echo "📋 Creating deployment..."
kubectl apply -f 03-deployment.yaml

echo "🌐 Creating service..."
kubectl apply -f 04-service.yaml

echo "📊 Creating autoscaler..."
kubectl apply -f 05-hpa.yaml

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Checking status..."
kubectl get all -n todos
echo ""
echo "🔍 To watch deployment progress:"
echo "   kubectl get pods -n todos -w"
echo ""
echo "📝 To check logs:"
echo "   kubectl logs -n todos -l app=todos-app --tail=50"
echo ""
echo "🌐 To get service IP:"
echo "   kubectl get service -n todos"
