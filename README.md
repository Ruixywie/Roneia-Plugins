# Roneia Plugins

Roneia v2 插件仓库。所有 Skill 使用 SKILL.md 格式定义，Server 从此仓库按需加载。

## 目录结构

```
roneia-plugins/
├── index.json                        # 插件索引（Server 首先读取，当前 11 个 Skill）
└── skills/
    ├── web_search_tavily/            # Tavily API 搜索（需 API Key）
    │   └── SKILL.md
    ├── web_search_ddg/               # DuckDuckGo 搜索（免费）
    │   ├── SKILL.md
    │   └── skill.ts
    ├── weather/                      # 天气查询（需 API Key）
    │   └── SKILL.md
    ├── url_reader/                   # 网页内容读取
    │   ├── SKILL.md
    │   └── skill.ts
    ├── calculator/                   # 数学计算（代码内嵌在 SKILL.md）
    │   └── SKILL.md
    ├── time_date/                    # 时间日期（代码内嵌在 SKILL.md）
    │   └── SKILL.md
    ├── filesystem/                   # 文件系统操作（Local Agent）
    │   └── SKILL.md
    ├── screenshot/                   # 屏幕截图 + 视觉理解（Local Agent）
    │   └── SKILL.md
    ├── clipboard/                    # 剪贴板读写（Local Agent）
    │   └── SKILL.md
    ├── shell/                        # Shell 命令执行（Local Agent）
    │   └── SKILL.md
    └── app_monitor/                  # 进程/应用监控（Local Agent）
        └── SKILL.md
```

## 内置 Skill 列表

### Server 端 Skill（6 个，Server 直接执行）

| 名称 | 类型 | 描述 | 需要 API Key |
|------|------|------|-------------|
| web_search_tavily | API | 使用 Tavily API 搜索互联网，获取最新信息和网页内容摘要 | TAVILY_API_KEY |
| web_search_ddg | Code | 使用 DuckDuckGo 搜索互联网，完全免费 | 否 |
| weather | API | 使用 OpenWeather API 查询全球城市的实时天气信息 | OPENWEATHER_API_KEY |
| url_reader | Code | 读取网页内容并提取纯文本，支持限制返回长度 | 否 |
| calculator | Code | 安全地计算数学表达式，支持基本运算和常见数学函数 | 否 |
| time_date | Code | 获取当前日期和时间，支持不同时区 | 否 |

Server 端 Skill 在 Server 端执行（`execution: server`），客户端无需安装任何依赖。

### Local Agent Skill（5 个，需要 Local Agent 二进制）

| 名称 | 类型 | 描述 | 需要 Local Agent |
|------|------|------|-----------------|
| filesystem | Code | 文件/目录操作（读写、列目录、搜索、移动、删除） | 是 |
| screenshot | Code | 截取屏幕画面，`capture_screen` 返回 base64 图像供 LLM 视觉理解 | 是 |
| clipboard | Code | 读取/写入系统剪贴板内容 | 是 |
| shell | Code | 执行 Shell 命令（含安全确认机制） | 是 |
| app_monitor | Code | 枚举/监控运行中的进程和应用窗口 | 是 |

Local Agent Skill 需要在用户机器上运行 Local Agent（Go 编译二进制，~5MB）。Server 通过 WebSocket 将工具调用转发给 Local Agent 执行，结果经 Local Agent 返回后再传给 LLM。

> **视觉理解**：`screenshot` Skill 的 `capture_screen` 工具返回 `output_type: 'image'`。Server 的 `toModelOutput` 函数将 base64 图像转换为 AI SDK 多模态内容格式，LLM 可直接"看到"截图进行视觉分析。

## Skill 类型

| 类型 | skill_type | 说明 | 示例 |
|------|------------|------|------|
| API Skill | `api` | 纯声明式，SKILL.md 描述 API 端点和参数映射，框架自动发 HTTP 请求 | weather, web_search_tavily |
| Code Skill | `code` | 服务端执行 TypeScript/JavaScript 代码（内嵌或独立 skill.ts）；Local Agent Skill 也属于此类，区别在于 `execution: local_agent` | web_search_ddg, url_reader, filesystem |
| Prompt Skill | `prompt` | 纯 LLM 指令，无可执行代码，仅影响 Agent 行为 | (暂无) |

### execution 字段

| 值 | 说明 |
|----|------|
| `server` | Server 直接执行（沙盒 JS 代码或声明式 API 调用） |
| `local_agent` | 通过 Local Agent 二进制在用户机器上执行，Server 通过 WebSocket 转发调用 |

### output_type 字段（Code Skill）

工具可声明 `output_type: 'image'`，表示返回 base64 编码的图像数据。Server 的 `toModelOutput` 函数会将其转换为 AI SDK 多模态内容格式（`image` part），使 LLM 能够进行视觉理解，无需额外处理。

## SKILL.md 格式

每个 Skill 由一个 `SKILL.md` 文件定义，包含 YAML frontmatter + 可选的 Instructions 和 Implementation 部分。

### API Skill 示例

```yaml
---
name: weather
version: 1.0.0
title: 天气查询
description: 查询城市天气
skill_type: api
execution: server
permissions: [network]
source: official
base_url: https://api.openweathermap.org
auth:
  type: query_param          # query_param | body_param | header | bearer
  param_name: appid
  env_key: OPENWEATHER_API_KEY
requires:
  env: [OPENWEATHER_API_KEY]
tools:
  - name: get_weather
    description: 查询天气
    method: GET
    endpoint: /data/2.5/weather
    parameters:
      q:
        type: string
        description: 城市名称
        required: true
---
```

### Code Skill 示例

```yaml
---
name: calculator
version: 1.0.0
title: 计算器
description: 计算数学表达式
skill_type: code
execution: server
permissions: []
source: official
tools:
  - name: calculate
    description: 计算数学表达式
    parameters:
      expression:
        type: string
        description: 数学表达式
        required: true
---

## Implementation

\```typescript
async function calculate(args: { expression: string }) {
  // ...实现代码
  return { success: true, result: { expression: args.expression, result: 42 } }
}
module.exports = { TOOLS: { calculate } }
\```
```

Code Skill 的代码可以内嵌在 SKILL.md 的 Implementation 块中，也可以放在独立的 `skill.ts` 文件中。代码在沙盒环境中执行，可用的全局对象包括 `fetch`（30s 超时 + 10MB 限制）、`console`、`Buffer`、`URL`、`JSON`、`Date`、`Math` 等。

## index.json 格式

`index.json` 是插件索引文件，Server 首先读取它来获取所有可用 Skill 的元数据。

```json
{
  "index_version": "2.0.0",
  "updated_at": "2026-03-11T00:00:00Z",
  "plugins": [
    {
      "id": "skill_name",
      "path": "skills/skill_name",
      "title": "显示名称",
      "description": "简短描述",
      "icon": "...",
      "version": "1.0.0",
      "skill_type": "api | code | prompt",
      "execution": "server | local_agent",
      "tags": ["tag1", "tag2"],
      "source": "official | community",
      "author": "作者名",
      "requires_env": ["ENV_KEY"],
      "requires_local_agent": false
    }
  ]
}
```

- `requires_env`：列出该 Skill 需要在 Server `.env` 中配置的环境变量。无需 API Key 的 Skill 使用空数组 `[]`。
- `requires_local_agent`：`true` 表示此 Skill 需要 Local Agent 在用户机器上运行。市场 UI 会显示"需要 Local Agent"徽章并在启用时弹出确认提示。

## 贡献新 Skill

1. Fork 本仓库
2. 在 `skills/` 下新建目录，创建 `SKILL.md`（API Skill 只需这一个文件；Code Skill 可额外添加 `skill.ts`）
3. 在 `index.json` 的 `plugins` 数组中添加对应条目
4. 提交 Pull Request

合并后，Server 调用 `POST /api/plugins/refresh-index` 即可热加载，无需重启。

## Server 配置

在 Server 的 `.env` 中配置：

```bash
PLUGINS_REPO=Ruixywie/roneia-plugins    # 指向此仓库
# PLUGINS_BRANCH=main

# Skill 需要的 API Key（按需配置）
# TAVILY_API_KEY=tvly-xxx
# OPENWEATHER_API_KEY=xxx
```
