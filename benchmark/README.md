# 性能测试模块

包含各种性能测试和优化对比测试。

## 测试文件

| 文件 | 说明 |
|------|------|
| `benchmark_test.go` | 基础性能测试 |
| `load_test.go` | 负载测试 |
| `cache_hit_test.go` | 缓存命中率测试 |
| `optimization_comparison_test.go` | 优化方案对比 |
| `rabbitmq_perf_test.go` | RabbitMQ 性能测试 |
| `performance_report.md` | 性能测试报告 |

## 运行测试

```bash
# 运行所有测试
go test -v ./benchmark/...

# 运行基准测试
go test -bench=. -benchmem ./benchmark/

# 运行负载测试
go test -v -run=LoadTest ./benchmark/

# 生成性能报告
go test -bench=. -benchmem -json > result.json
```

## 测试内容

### 1. 基准测试 (benchmark_test.go)

测试各核心操作性能：

- JSON 序列化/反序列化
- Redis 读写
- MySQL 查询
- 内存分配

### 2. 负载测试 (load_test.go)

模拟真实场景：

- 并发用户数：100/500/1000
- 测试时长：30s/1m/5m
- QPS 监控

### 3. 缓存命中率 (cache_hit_test.go)

```go
// 测试缓存命中率
func TestCacheHitRate() {
    // 写入测试数据
    for i := 0; i < 10000; i++ {
        Set(key, value)
    }

    // 读取（部分命中）
    for i := 0; i < 10000; i++ {
        Get(key)
    }

    // 计算命中率
    hitRate := hits / total
}
```

### 4. 优化对比 (optimization_comparison_test.go)

对比不同优化方案效果：

| 优化项 | 原始 | 优化后 | 提升 |
|--------|------|--------|------|
| JSON 库 | encoding/json | json-iterator | 3x |
| Redis 连接 | 单连接 | 连接池 | 5x |
| GOMAXPROCS | 1 | 8 | 2x |

### 5. RabbitMQ 测试 (rabbitmq_perf_test.go)

- 消息发送吞吐量
- 消费延迟
- 队列积压处理

## 性能指标

### 目标 QPS

| 接口 | 目标 QPS |
|------|----------|
| 短链查询 | 61000+ |
| 短链创建 | 5000 |
| AI 对话 | 500 |

### 延迟指标

| 指标 | P50 | P95 | P99 |
|------|-----|-----|-----|
| 接口延迟 | <10ms | <50ms | <100ms |
| AI 对话 | <3s | <10s | <30s |

## 优化实践

### 1. JSON 序列化

```go
// 标准库
json.Marshal(data)  // 慢

// json-iterator
import jsoniter "github.com/json-iterator/go"
jsoniter.Marshal(data)  // 快 3-10x
```

### 2. Redis 连接池

```go
redis.NewClient(&redis.Options{
    PoolSize: 100,      // 连接池大小
    MinIdleConns: 10,   // 最小空闲连接
})
```

### 3. GOMAXPROCS

```bash
# 设置为 CPU 核数
export GOMAXPROCS=$(nproc)

# 或代码中设置
runtime.GOMAXPROCS(runtime.NumCPU())
```

### 4. 短链生成优化

```go
// 预生成号段，避免锁竞争
type ShortLinkGenerator struct {
    current int64
    max     int64
    mu      sync.Mutex
}

func (g *ShortLinkGenerator) Next() string {
    g.mu.Lock()
    defer g.mu.Unlock()
    if g.current >= g.max {
        g.refill()
    }
    return base62.Encode(g.current++)
}
```

## 测试报告

详见 `performance_report.md`

## 压测工具

推荐使用：

- **wrk** - 简单 HTTP 基准测试
- **k6** - 可编程负载测试
- **vegeta** - 恒定速率攻击测试

```bash
# wrk 示例
wrk -t12 -c400 -d30s http://localhost:8080/api/v1/shorturl/query?short=abc123

# k6 示例
k6 run --vus 100 --duration 30s script.js
```

## 常见问题

### 1. 压测结果不稳定

- 预热后再测试
- 多次测试取平均值
- 排除网络波动影响

### 2. 无法达到目标 QPS

- 检查 CPU 是否打满
- 检查连接池配置
- 检查上游服务限制
