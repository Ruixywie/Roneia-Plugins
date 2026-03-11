# Roneia Plugins

Roneia v2 能力包（Ability Pack）仓库。所有能力包使用 ABILITY.md 格式定义，Server 从此仓库按需加载。

## 目录结构

```
roneia-plugins/
├── index.json                        # 能力包索引（Server 首先读取，当前 11 个）
└── skills/
    ├── web_search_tavily/            # Tavily API 搜索（需 API Key）
    │   └── ABILITY.md
    ├── web_search_ddg/               # DuckDuckGo 搜索（免费）
    │   ├── ABILITY.md
    │   └── skill.ts
    ├── weather/                      # 天气查询（需 API Key）
    │   └── ABILITY.md
    ├── url_reader/                   # 网页内容读取
    │   ├── ABILITY.md
    │   └── skill.ts
    ├── calculator/                   # 数学计算（代码内嵌在 ABILITY.md）
    │   └── ABILITY.md
    ├── time_date/                    # 时间日期（代码内嵌在 ABILITY.md）
    │   └── ABILITY.md
    ├── filesystem/                   # 文件系统操作（需 Local Agent）
    │   └── ABILITY.md
    ├── screenshot/                   # 屏幕截图 + 视觉理解（需 Local Agent）
    │   └── ABILITY.md
    ├── clipboard/                    # 剪贴板读写（需 Local Agent）
    │   └── ABILITY.md
    ├── shell/                        # Shell 命令执行（需 Local Agent）
    │   └── ABILITY.md
    └── app_monitor/                  # 应用窗口监控（需 Local Agent）
        └── ABILITY.md
```

## 内置能力包列表

### Server 端能力包（6 个）

| 名称 | 执行方式 | 描述 | 需要 API Key |
|------|---------|------|-------------|
| web_search_tavily | API 声明式 | 使用 Tavily API 搜索互联网 | TAVILY_API_KEY |
| web_search_ddg | Code 沙盒 | 使用 DuckDuckGo 搜索，完全免费 | 否 |
| weather | API 声明式 | 使用 OpenWeather API 查询天气 | OPENWEATHER_API_KEY |
| url_reader | Code 沙盒 | 读取网页内容并提取纯文本 | 否 |
| calculator | Code 内嵌 | 安全地计算数学表达式 | 否 |
| time_date | Code 内嵌 | 获取当前日期和时间 | 否 |

### Local Agent 能力包（5 个，需要 Local Agent 二进制）

| 名称 | 描述 | Provider 工具 |
|------|------|--------------|
| filesystem | 文件读写、浏览目录、搜索文件 | `local_fs_read`, `local_fs_write`, `local_fs_list`, `local_fs_search`, `local_open` |
| screenshot | 截取屏幕画面并支持 AI 视觉理解 | `local_screenshot`, `local_screenshot_displays` |
| clipboard | 读取/写入系统剪贴板内容 | `local_clipboard_read`, `local_clipboard_write` |
| shell | 执行 Shell 命令（含安全确认） | `local_shell_exec` |
| app_monitor | 检测当前活动应用窗口 | `local_app_active` |

Local Agent 能力包声明 `requires: [local]`，系统自动注入 local Provider 的工具（共 11 个）。多个能力包需要同一 Provider 时，工具只注入一次（去重）。

> **视觉理解**：`screenshot` 的 `local_screenshot` 工具声明 `output_type: 'image'`，Server 的 `toModelOutput` 将 base64 图像转为 AI SDK 多模态格式，LLM 可直接视觉分析。

## Ability Pack + Provider 架构

### Provider（系统内建）

| Provider | 职责 |
|----------|------|
| `local` | Go Agent 系统原语（11 个 `local_*` 工具） |
| `http` | API 类能力包的 HTTP 执行引擎 |
| `runtime` | Code 类能力包的 JS 沙盒执行引擎 |

### 执行方式推断

系统根据 ABILITY.md 内容自动推断执行方式，无需显式声明 `skill_type` 或 `execution`：

| 内容特征 | 推断结果 |
|---------|---------|
| `requires: [local]` | 需要 Local Agent，注入 local Provider 工具 |
| `api:` + `tools:` 带 `endpoint` | 声明式 HTTP 调用 |
| `tools:` + `## Implementation` | Code 沙盒执行 |
| 仅 `## Instructions` | 纯 LLM 指令 |

## ABILITY.md 格式

每个能力包由一个 `ABILITY.md` 文件定义，包含 YAML frontmatter + 可选的 Instructions 和 Implementation 部分。

### API 能力包示例

```yaml
---
name: weather
version: 1.0.0
title: 天气查询
description: 查询城市天气
requires_env: [OPENWEATHER_API_KEY]
permissions: [network]
api:
  base_url: https://api.openweathermap.org
  auth:
    type: query_param
    param_name: appid
    env_key: OPENWEATHER_API_KEY
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

### Code 能力包示例

```yaml
---
name: calculator
version: 1.0.0
title: 计算器
description: 计算数学表达式
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
  return { success: true, result: eval(args.expression) }
}
module.exports = { TOOLS: { calculate } }
\```
```

### Local Agent 能力包示例

```yaml
---
name: filesystem
version: 1.0.0
title: 文件管理
description: 文件读写和目录管理
requires: [local]
---

## Instructions
使用 local_fs_read 读取文件，local_fs_write 写入文件，local_fs_list 列出目录。
```

Local Agent 能力包不定义自己的工具，而是通过 `requires: [local]` 声明依赖 local Provider，系统自动注入对应工具。

## index.json 格式

```json
{
  "index_version": "3.0.0",
  "updated_at": "2026-03-11T00:00:00Z",
  "plugins": [
    {
      "id": "skill_name",
      "path": "skills/skill_name",
      "title": "显示名称",
      "description": "简短描述",
      "icon": "...",
      "version": "1.0.0",
      "tags": ["tag1", "tag2"],
      "source": "official",
      "author": "作者名",
      "requires": ["local"],
      "requires_env": ["ENV_KEY"]
    }
  ]
}
```

- `requires`：声明依赖的 Provider（如 `["local"]`），无依赖则省略
- `requires_env`：需要在 Server `.env` 中配置的环境变量

## 贡献新能力包

1. Fork 本仓库
2. 在 `skills/` 下新建目录，创建 `ABILITY.md`
3. 在 `index.json` 的 `plugins` 数组中添加条目
4. 提交 Pull Request

合并后，Server 调用 `POST /api/plugins/refresh-index` 即可热加载，无需重启。

## Server 配置

在 Server 的 `.env` 中配置：

```bash
PLUGINS_REPO=Ruixywie/roneia-plugins    # 指向此仓库
# PLUGINS_BRANCH=main

# 能力包需要的 API Key（按需配置）
# TAVILY_API_KEY=tvly-xxx
# OPENWEATHER_API_KEY=xxx
```
