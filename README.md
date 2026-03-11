# Roneia Plugins

Roneia v2 插件仓库。Server 启动时从此仓库动态加载所有 Skill 的定义和代码。

## 目录结构

```
roneia-plugins/
├── index.json                        # 插件索引（Server 首先读取）
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
    ├── calculator/                   # 数学计算
    │   └── SKILL.md                  # implementation 内嵌
    └── time_date/                    # 时间日期
        └── SKILL.md                  # implementation 内嵌
```

## Skill 类型

| 类型 | skill_type | 说明 | 示例 |
|------|------------|------|------|
| API Skill | `api` | 纯声明式，SKILL.md 描述 API 端点和参数映射，框架自动发 HTTP 请求 | weather, web_search_tavily |
| Code Skill | `code` | 服务端执行 TypeScript/JavaScript 代码 | web_search_ddg, url_reader, calculator |
| Prompt Skill | `prompt` | 纯 LLM 指令，无可执行代码，仅影响 Agent 行为 | (暂无) |

所有 Skill 在 Server 端执行（`execution: server`），客户端无需安装任何依赖。

## SKILL.md 格式

每个 Skill 由一个 `SKILL.md` 文件定义，包含 YAML frontmatter + 可选的 Instructions 和 Implementation 部分：

```markdown
---
name: my_skill
version: 1.0.0
title: 我的技能
description: 这个技能做什么
icon: "🔧"
category: utility
author: YourName
tags: [tag1, tag2]
skill_type: code          # api | code | prompt
execution: server          # server | local_agent | client
permissions: [network]     # 需要的权限
source: official           # official | community

# API Skill 特有字段
base_url: https://api.example.com
auth:
  type: query_param        # query_param | body_param | header | bearer
  param_name: key
  env_key: MY_API_KEY
requires:
  env: [MY_API_KEY]

tools:
  - name: do_something
    description: 做某件事
    method: GET             # API Skill: HTTP 方法
    endpoint: /endpoint     # API Skill: API 路径
    parameters:
      param1:
        type: string
        description: 参数描述
        required: true
---

## Instructions

给 LLM 的使用指导。

## Implementation

\`\`\`typescript
// Code Skill: 内嵌实现代码
async function do_something(args) {
  return { success: true, result: ... }
}
module.exports = { TOOLS: { do_something } }
\`\`\`
```

### Code Skill 代码文件

对于复杂的 Code Skill，代码可以放在独立的 `skill.ts` 文件中（而非内嵌在 SKILL.md 的 Implementation 块）。

代码在沙盒环境中执行，可用的全局对象：
- `fetch` — 安全封装，30s 超时，10MB 大小限制
- `console` — log/warn/error/debug
- `Buffer`, `URL`, `URLSearchParams`
- `TextEncoder`, `TextDecoder`, `AbortController`
- `JSON`, `Date`, `Math`, `setTimeout`, `clearTimeout`

代码需要导出 `TOOLS` 对象：
```typescript
module.exports = {
  TOOLS: {
    tool_name: async (args) => {
      return { success: true, result: { ... } }
    }
  }
}
```

## 添加新 Skill

1. 在 `skills/` 下新建目录
2. 创建 `SKILL.md`（API Skill 只需这一个文件；Code Skill 可额外添加 `skill.ts`）
3. 在 `index.json` 中添加条目
4. 推送到 GitHub

Server 调用 `POST /api/plugins/refresh-index` 即可热加载，无需重启。

## Server 配置

在 Server 的 `.env` 中配置：

```bash
PLUGINS_REPO=Ruixywie/roneia-plugins    # 指向此仓库
# PLUGINS_BRANCH=main

# Skill 需要的 API Key（按需配置）
# TAVILY_API_KEY=tvly-xxx
# OPENWEATHER_API_KEY=xxx
```
