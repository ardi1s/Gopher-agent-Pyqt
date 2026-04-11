# AI Helper 模块

AI 助手核心模块，负责管理多模型 AI 对话能力。

## 架构设计

采用**工厂模式** + **单例模式**：

```
AIHelperFactory     - 根据 modelType 创建不同的 AI Helper
AIHelperManager    - 全局单例，管理所有用户的会话
AIHelper           - 具体对话逻辑实现
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `factory.go` | 工厂类，根据 modelType 创建对应 Helper |
| `manager.go` | 全局管理器，管理用户与会话的映射关系 |
| `aihelper.go` | AI Helper 接口定义和实现 |
| `model.go` | 数据模型定义 |

## 模型类型

| modelType | 模型 | 说明 |
|-----------|------|------|
| `1` | 阿里百炼 | 普通 LLM 对话 |
| `2` | RAG 模型 | 知识库检索增强回答 |
| `3` | MCP 模型 | 工具调用增强回答 |

## AIHelperManager

全局会话管理器，线程安全：

```go
type AIHelperManager struct {
    helpers map[string]map[string]*AIHelper  // map[用户]map[会话ID]*Helper
    mu      sync.RWMutex
}
```

**核心方法：**

- `GetOrCreateAIHelper()` - 获取或创建 Helper
- `GetAIHelper()` - 获取指定用户的指定会话
- `RemoveAIHelper()` - 移除会话
- `GetUserSessions()` - 获取用户所有会话

## 使用示例

```go
// 获取全局管理器
manager := aihelper.GetGlobalManager()

// 创建或获取 Helper
config := map[string]interface{}{
    "apiKey": "your-api-key",
    "username": userName,
}
helper, err := manager.GetOrCreateAIHelper(userName, sessionID, modelType, config)

// 发送消息
response, err := helper.GenerateResponse(ctx, userQuestion)

// 流式发送
helper.StreamResponse(ctx, callback, prompt)
```

## 消息管理

每个 AIHelper 维护自己的对话历史：

```go
helper.AddMessage(content, username, isUser, storeToDB)
messages := helper.GetMessages()
```

`storeToDB` 参数控制是否持久化到数据库。

## 初始化

服务启动时从数据库加载历史消息：

```go
// main.go
readDataFromDB()  // 加载所有消息到内存
```

## 注意事项

1. **线程安全** - 使用 RWMutex 保护并发读写
2. **模型切换** - modelType 变化时会重建 Helper
3. **内存管理** - 会话删除时需同步清理 Helper
