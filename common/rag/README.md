# RAG 知识库模块

基于 Redis Search 的 RAG（Retrieval Augmented Generation）知识库实现。

## 核心概念

RAG = 检索增强生成

```
用户问题 → 向量检索 → 相关文档 → 拼入 Prompt → LLM 生成回答
```

## 技术方案

**向量存储**：Redis Search 模块（RediSearch）
**向量模型**：火山引擎 Embedding API
**检索算法**：余弦相似度（Cosine）

## 工作流程

### 1. 文档索引

```
用户上传文档（.md/.txt）
    ↓
文本切分
    ↓
调用 Embedding API 生成向量
    ↓
存储到 Redis（RediSearch 向量索引）
```

### 2. 知识查询

```
用户提问
    ↓
问题向量化（Embedding）
    ↓
Redis 向量相似度检索（TopK=5）
    ↓
获取相关文档内容
    ↓
拼入 Prompt → LLM 生成回答
```

## 核心实现

### 创建索引

```go
func InitRedisIndex(ctx context.Context, filename string, dimension int) error {
    // 创建 RediSearch 向量索引
    createArgs := []interface{}{
        "FT.CREATE", indexName,
        "ON", "HASH",
        "PREFIX", "1", prefix,
        "SCHEMA",
        "content", "TEXT",
        "metadata", "TEXT",
        "vector", "VECTOR", "FLAT",
        "6",  // 算法参数
        "TYPE", "FLOAT32",
        "DIM", dimension,        // 向量维度
        "DISTANCE_METRIC", "COSINE",
    }
}
```

### 文档存储

```go
// DocumentToHashes 定义文档如何存储到 Redis
DocumentToHashes: func(ctx context.Context, doc *schema.Document) (*redisIndexer.Hashes, error) {
    return &redisIndexer.Hashes{
        Key: fmt.Sprintf("%s:%s", filename, doc.ID),
        Field2Value: map[string]redisIndexer.FieldValue{
            "content": {Value: doc.Content, EmbedKey: "vector"},  // 自动向量化
            "metadata": {Value: source},
        },
    }, nil
}
```

### 向量检索

```go
// 创建 Retriever
retrieverConfig := &redisRetriever.RetrieverConfig{
    Client:       rdb,
    Index:       indexName,
    Dialect:     2,              // RediSearch v2
    ReturnFields: []string{"content", "metadata", "distance"},
    TopK:        5,              // 返回 Top 5 相关文档
    VectorField: "vector",
}

// 检索
docs, err := retriever.Retrieve(ctx, query)
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `rag.go` | RAG 索引器和查询器实现 |

## 配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `RagApiKey` | 火山引擎 API Key | - |
| `RagBaseUrl` | 向量模型服务地址 | - |
| `RagEmbeddingModel` | Embedding 模型名 | - |
| `RagDimension` | 向量维度 | 1536 |

## 优势与局限

### 优势
- 部署简单，基于 Redis
- 支持混合检索（向量 + 全文）
- 内存级存储，延迟低

### 局限
- Redis 向量检索性能不如专业向量数据库
- 数据量级建议在百万以下
- 不支持分布式向量索引

## 扩展方向

- [ ] 支持 Milvus、Pinecone 等专业向量数据库
- [ ] 文本切分策略优化
- [ ] 混合检索策略调优
