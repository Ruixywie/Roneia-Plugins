# Roneia Plugins

Roneia 插件仓库。Server 启动时从此仓库动态加载所有插件的 manifest 和代码。

## 目录结构

```
roneia-plugins/
├── index.json                 # 插件索引（Server 首先读取）
├── skills/                    # 技能插件
│   ├── local_file/
│   │   ├── manifest.json      # 元数据 + 工具定义
│   │   └── skill.py           # 代码式实现
│   ├── web_search/
│   │   ├── manifest.json
│   │   └── skill.py
│   ├── screen_capture/
│   │   ├── manifest.json
│   │   └── skill.py
│   └── weather/
│       └── manifest.json      # API 式，无 .py
└── components/                # 组件插件
    └── voice/
        └── manifest.json      # 组件元数据 + 依赖声明
```

## 插件类型

| 类型 | plugin_type | skill_type | 说明 |
|------|-------------|------------|------|
| 代码式 Skill | skill | code | manifest.json + skill.py，Client 下载代码执行 |
| 声明式 API Skill | skill | api | 仅 manifest.json，框架自动发 HTTP 请求 |
| 组件 | component | code | 仅 manifest.json + 依赖声明，Client 安装依赖 |

## 添加新插件

1. 在 `skills/` 或 `components/` 下新建目录
2. 创建 `manifest.json`（代码式还需 `skill.py`）
3. 在 `index.json` 中添加条目
4. 推送到 GitHub

Server 调用 `POST /api/plugins/refresh-index` 即可热加载，无需重启。

## Server 配置

在 Server 的 `.env` 中配置：

```
PLUGINS_REPO=Ruixywie/roneia-plugins
PLUGINS_BRANCH=main
```
