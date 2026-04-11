# Docker 部署

使用 Docker Compose 进行本地开发和部署。

## 目录结构

```
deploy/docker/
├── Dockerfile              # 后端镜像构建
├── Dockerfile.frontend    # 前端镜像构建
├── docker-compose.yml      # 生产环境编排
├── docker-compose.dev.yml # 开发环境编排
├── nginx.conf            # Nginx 配置
├── ca-certificates.crt   # CA 证书
└── .dockerignore         # Docker 忽略文件
```

## 快速开始

### 开发环境

```bash
cd deploy/docker

# 启动所有服务
docker-compose -f docker-compose.dev.yml up -d

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f

# 停止服务
docker-compose -f docker-compose.dev.yml down
```

### 生产环境

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

## 服务组件

| 服务 | 镜像 | 端口 |
|------|------|------|
| backend | golang:alpine | 8080 |
| frontend | nginx:alpine | 80 |
| mysql | mysql:8.0 | 3306 |
| redis | redis:7-alpine | 6379 |
| rabbitmq | rabbitmq:3-management | 5672, 15672 |

## Nginx 配置

前端请求转发：

```nginx
location /api/ {
    proxy_pass http://backend:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location / {
    root /usr/share/nginx/html;
    index index.html;
}
```

## 环境变量

```bash
# 后端
MYSQL_HOST=mysql
MYSQL_PORT=3306
REDIS_HOST=redis
REDIS_PORT=6379
RABBITMQ_HOST=rabbitmq

# 前端
VITE_API_BASE_URL=http://localhost:8080
```

## 数据持久化

```yaml
volumes:
  mysql_data:
  redis_data:
```

## 健康检查

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 常见问题

### 1. MySQL 连接失败

确保 MySQL 初始化完成后再启动后端：

```yaml
depends_on:
  mysql:
    condition: service_healthy
```

### 2. 前端无法访问后端

检查 Nginx 代理配置和后端健康状态。

### 3. 端口冲突

修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8081:8080"  # 后端
```

## 扩展开发

### 添加新服务

1. 在 `docker-compose.yml` 中添加服务定义
2. 创建对应的 Dockerfile
3. 重启 docker-compose

### 调整资源限制

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```
