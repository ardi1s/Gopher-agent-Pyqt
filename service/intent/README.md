# 意图识别模块

自动识别用户问题意图，实现智能分流。

## 设计背景

用户提问方式多样，需要根据意图选择合适的 AI 模型处理：

- 普通聊天 → 直接用 LLM 回答
- 需要查知识库 → 路由到 RAG 模型
- 需要调用工具 → 路由到 MCP 模型

## 识别方案

使用**轻量级模型**做意图识别，成本低、速度快：

```go
// 使用 qwen-turbo 做意图识别
model := "qwen-turbo"
intentRecognizer = intent.NewIntentRecognizer(apiKey, baseURL, model)
```

## 意图类型

| 意图类型 | 说明 | 路由模型 |
|---------|------|----------|
| `IntentChat` | 普通对话 | 模型1（阿里百炼） |
| `IntentRAG` | 知识库问答 | 模型2（RAG） |
| `IntentMCP` | 工具调用 | 模型3（MCP） |

## 工作流程

```
用户提问
    ↓
IntentRecognizer.Recognize()
    ↓
调用轻量模型分析意图
    ↓
返回 IntentResult
    ↓
根据 Type 路由到对应模型
```

## IntentResult 结构

```go
type IntentResult struct {
    Type     IntentType  // 意图类型
    Tool     string      // 需要的工具（如果是 MCP）
    Workflow string      // 工作流类型（如 RAG+MCP）
    // ...
}
```

## 工作流类型

| 工作流类型 | 说明 |
|-----------|------|
| `WorkflowDefault` | 默认流程 |
| `WorkflowRAGMCP` | RAG + MCP 联动 |

## 使用示例

```go
// 初始化（main.go）
func init() {
    apiKey := os.Getenv("OPENAI_API_KEY")
    baseURL := os.Getenv("OPENAI_BASE_URL")
    model := "qwen-turbo"

    intentRecognizer = intent.NewIntentRecognizer(apiKey, baseURL, model)
}

// 使用
intentResult, err := intentRecognizer.Recognize(ctx, question)
if intentResult.Type == intent.IntentRAG {
    // 路由到 RAG 模型
}
```

## 优化策略

1. **轻量模型** - 用 qwen-turbo，成本低
2. **缓存结果** - 相同问题不重复识别
3. **降级策略** - 识别失败默认走普通聊天

## 文件说明

| 文件 | 说明 |
|------|------|
| `intent.go` | 意图识别核心实现 |

## 扩展方向

- [ ] 支持更多意图类型
- [ ] 自定义识别规则
- [ ] 多语言支持
