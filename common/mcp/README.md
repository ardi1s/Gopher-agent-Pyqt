# MCP 服务端模块

MCP（Model Context Protocol）协议服务端实现，用于 AI 模型调用外部工具。

## 什么是 MCP？

MCP 是 **Model Context Protocol** 的缩写，是一个让 AI 模型调用外部工具的协议标准。

```
AI 模型 ←→ MCP Server ←→ 外部工具（数据库、API、文件系统等）
```

## 协议特点

| 特性 | 说明 |
|------|------|
| JSON-RPC 2.0 | 基于 JSON 的远程调用协议 |
| 工具注册 | 标准化工具定义和调用方式 |
| 双向通信 | 支持服务端主动推送 |

## 目录结构

```
mcp/
├── main.go           # MCP 服务入口
├── server/
│   └── server.go     # MCP 服务端实现
├── client/
│   └── client.go     # MCP 客户端实现
├── go.mod
└── go.sum
```

## 工作流程

```
1. MCP Server 启动，注册可用工具
2
3. AI 模型判断需要调用工具，返回 tool call
4. 后端通过 MCP Client 调用工具
5. 工具执行结果返回给 LLM
6. LLM 生成最终回答
```

## 工具定义示例

```json
{
  "name": "get_weather",
  "description": "获取城市天气信息",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "城市名称"
      }
    }
  }
}
```

## 使用示例

```go
// 创建 MCP Helper（通过工厂模式）
mcpHelper, err := manager.GetOrCreateAIHelper(userName, sessionID, "3", config)

// 调用工具
result, err := mcpHelper.CallTool(ctx, "get_weather", map[string]interface{}{
    "city": "北京",
})
```

## RAG + MCP 联动

项目实现了 RAG + MCP 联动工作流：

```
用户问题
    ↓
RAG 检索相关文档
    ↓
MCP 调用工具（如查天气）
    ↓
合并结果，生成增强 Prompt
    ↓
LLM 生成最终回答
```

## 与 gRPC 的区别

| | MCP | gRPC |
|--|-----|------|
| 设计目标 | AI 与工具交互 | 微服务通信 |
| 协议 | JSON-RPC 2.0 | Protocol Buffers |
| 语义 | 内置 tools/resources | 通用 RPC |

## 扩展工具

只需在 `server.go` 中注册新工具即可：

```go
func (s *Server) registerTools() {
    s.tools["get_weather"] = GetWeatherTool
    s.tools["query_database"] = QueryDatabaseTool
    // 添加更多工具...
}
```

## 注意事项

1. **安全性** - 工具调用需权限控制
2. **超时** - 工具执行要有超时保护
3. **错误处理** - 工具失败要优雅降级
