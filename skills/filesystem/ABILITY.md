---
name: filesystem
version: 1.0.0
title: 文件管理
description: 读写文件、浏览目录、搜索文件和用默认程序打开文件
icon: "📁"
category: system
author: Ruixywie
tags: [file, filesystem, system, local]
requires: [local]
permissions: [filesystem]
source: official
---

## Instructions

文件管理能力包在用户本地机器上执行，需要 Local Agent 运行。
文件操作受路径限制——只能访问 Local Agent 启动时配置的允许目录。

可用工具：
- `local_fs_read` - 读取文件内容（限制 100KB）
- `local_fs_write` - 将内容写入文件（会覆盖已有内容）
- `local_fs_list` - 列出目录中的文件和子目录
- `local_fs_search` - 在目录中递归搜索匹配模式的文件（最多 50 个结果）
- `local_open` - 用系统默认程序打开文件
