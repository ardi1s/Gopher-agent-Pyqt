# Kubernetes 部署

生产环境使用 K8s 进行容器编排和服务管理。

## 目录结构

```
deploy/k8s/
├── namespace.yaml      # 命名空间
├── configmap.yaml       # 配置
├── secret.yaml         # 密钥
├── mysql.yaml          # MySQL 有状态服务
├── redis.yaml          # Redis 服务
├── rabbitmq.yaml       # RabbitMQ 服务
├── backend.yaml        # 后端无状态服务
├── frontend.yaml       # 前端服务
├── ingress.yaml        # Ingress 入口
└── kustomization.yaml # Kustomize 配置
```

## 快速部署

```bash
cd deploy/k8s

# 应用所有配置
kubectl apply -k .

# 查看 pods
kubectl get pods -n gopherai

# 查看日志
kubectl logs -n gopherai -l app=backend -f
```

## 组件说明

### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: gopherai
```

### ConfigMap

存储非敏感配置：

```yaml
data:
  MYSQL_HOST: "mysql"
  REDIS_HOST: "redis"
  RABBITMQ_HOST: "rabbitmq"
```

### Secret

存储敏感信息：

```yaml
data:  # Base64 编码
  MYSQL_PASSWORD: xxx
  REDIS_PASSWORD: xxx
  RABBITMQ_PASSWORD: xxx
```

### Backend

后端 Deployment：

```yaml
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    spec:
      containers:
      - name: backend
        image: gopherai/backend:latest
        ports:
        - containerPort: 8080
```

### Frontend

前端 Deployment + Service：

```yaml
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: frontend
        image: gopherai/frontend:latest
        ports:
        - containerPort: 80
```

### Ingress

外部访问入口：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gopherai-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: gopherai.example.com
    http:
      paths:
      - path: /api/
        backend:
          service:
            name: backend
            port:
              number: 8080
      - path: /
        backend:
          service:
            name: frontend
            port:
              number: 80
```

## 数据存储

### MySQL

有状态服务，使用 PVC 持久化：

```yaml
kind: StatefulSet
spec:
  serviceName: mysql
  replicas: 1
  volumeClaimTemplates:
  - metadata:
      name: mysql-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### Redis

同样使用 PVC：

```yaml
volumeClaimTemplates:
- metadata:
    name: redis-data
  spec:
    accessModes: ["ReadWriteOnce"]
    resources:
      requests:
        storage: 5Gi
```

## 扩缩容

```bash
# 扩容后端到 5 个副本
kubectl scale deployment backend --replicas=5 -n gopherai

# 扩容 MySQL（不建议）
kubectl scale statefulset mysql --replicas=2 -n gopherai
```

## 更新部署

```bash
# 更新镜像
kubectl set image deployment/backend backend=gopherai/backend:v2 -n gopherai

# 查看更新进度
kubectl rollout status deployment/backend -n gopherai

# 回滚
kubectl rollout undo deployment/backend -n gopherai
```

## 资源限制

```yaml
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 1Gi
```

## 健康检查

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 常见问题

### 1. Pod 无法启动

```bash
kubectl describe pod <pod-name> -n gopherai
kubectl logs <pod-name> -n gopherai
```

### 2. 无法连接 MySQL

检查 MySQL Pod 状态和服务是否正常：

```bash
kubectl get pods -l app=mysql -n gopherai
kubectl get svc mysql -n gopherai
```

### 3. Ingress 不工作

检查 Ingress 控制器是否部署：

```bash
kubectl get ingressclass
kubectl describe ingress gopherai-ingress -n gopherai
```

## 使用 Kustomize

```bash
# 查看差异
kubectl diff -k .

# 应用
kubectl apply -k .
```
