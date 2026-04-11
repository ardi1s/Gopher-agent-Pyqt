# 会话服务模块

核心业务模块，处理 AI 对话相关的业务逻辑。

## 功能概述

| 功能 | 说明 |
|------|------|
| 创建会话 | 创建新的聊天会话 |
| 发送消息 | 普通模式发送消息 |
| 流式消息 | SSE 流式响应 |
| 会话历史 | 获取和展示聊天历史 |
| 删除会话 | 清理会话及关联数据 |
| 意图识别 | 自动识别用户意图并分流 |

## 核心流程

### 1. 创建会话并发送消息

```
CreateSessionAndSendMessage(userName, userQuestion, modelType)
    ↓
检测 modelType（auto 或指定）
    ↓
创建新会话（MySQL）
    ↓
获取/创建 AIHelper
    ↓
调用 LLM 生成回答
    ↓
返回 (sessionID, answer, modelType, code)
```

### 2. 流式消息发送

```
StreamMessageToExistingSession(...)
    ↓
意图识别（detectModelType）
    ↓
检查是否 RAG+MCP 联动工作流
    ↓
获取 AIHelper
    ↓
SSE 流式调用 StreamResponse
    ↓
实时推送数据块给前端
```

### 3. 意图识别分流

```go
func detectModelType(question string) string {
    // 使用轻量级模型识别意图
    intentResult, _ := intentRecognizer.Recognize(ctx, question)

    switch intentResult.Type {
    case IntentRAG:
        return "2"  // RAG 模型
    case IntentMCP:
        return "3"  // MCP 模型
    default:
        return "1"  // 普通聊天
    }
}
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `session.go` | 会话核心业务逻辑 |
| `workflow.go` | RAG + MCP 联动工作流 |

## API 接口

### 创建会话并发送

```
POST /api/v1/AI/chat/send-new-session
```

参数：
- `username`: 用户名
- `question`: 问题
- `modelType`: 模型类型（1/2/3/auto）

### 发送消息（已有会话）

```
POST /api/v1/AI/chat/send
```

参数：
- `username`: 用户名
- `sessionId`: 会话 ID
- `question`: 问题
- `modelType`: 模型类型

### 流式发送

```
POST /api/v1/AI/chat/send-stream
POST /api/v1/AI/chat/send-stream-new-session
```

响应：SSE 流式数据

### 获取会话列表

```
GET /api/v1/AI/chat/sessions
```

### 获取聊天历史

```
POST /api/v1/AI/chat/history
```

### 删除会话

```
DELETE /api/v1/AI/chat/session
```

## 联动工作流

`workflow.go` 实现了 RAG + MCP 联动：

```go
func executeRAGMCPWorkflow(...) code.Code {
    // 1. RAG 检索
    ragResult, _ := callRAGSearch(helper, ctx, question)

    // 2. MCP 工具调用
    mcpResult, _ := callMCPCallTool(helper, ctx, toolName, args)

    // 3. 合并结果生成回答
    enhancedPrompt := fmt.Sprintf(
        `【相关知识】%s\n【工具结果】%s\n【用户问题】%s`,
        ragResult, mcpResult, question
    )

    // 4. 流式返回
    chatHelper.StreamResponse(ctx, cb, enhancedPrompt)
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| `CodeSuccess` | 成功 |
| `CodeServerBusy` | 服务器繁忙 |
| `AIModelFail` | AI 模型调用失败 |

## 依赖模块

- `aihelper` - AI 对话能力
- `dao/session` - 会话数据访问
- `dao/message` - 消息数据访问
- `intent` - 意图识别
