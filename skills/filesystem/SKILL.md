---
name: filesystem
version: 1.0.0
title: 文件管理
description: 读写文件、浏览目录、搜索文件和用默认程序打开文件
icon: "📁"
category: system
author: Ruixywie
tags: [file, filesystem, system, local]
skill_type: code
execution: local_agent
permissions: [filesystem]
source: official
tools:
  - name: read_file
    description: 读取文件内容（限制 100KB）
    parameters:
      path:
        type: string
        description: 文件的绝对路径或相对路径
        required: true
  - name: write_file
    description: 将内容写入文件（会覆盖已有内容）
    parameters:
      path:
        type: string
        description: 文件路径
        required: true
      content:
        type: string
        description: 要写入的文件内容
        required: true
  - name: list_dir
    description: 列出目录中的文件和子目录
    parameters:
      path:
        type: string
        description: 目录路径
        required: true
  - name: search_files
    description: 在目录中递归搜索匹配模式的文件（最多 50 个结果）
    parameters:
      directory:
        type: string
        description: 搜索的起始目录
        required: true
      pattern:
        type: string
        description: "文件名匹配模式（如 *.txt, *.py）"
        required: true
  - name: open_file
    description: 用系统默认程序打开文件
    parameters:
      path:
        type: string
        description: 要打开的文件路径
        required: true
---

## Instructions

文件管理工具在用户本地机器上执行，需要 Local Agent 运行。
文件操作受路径限制——只能访问 Local Agent 启动时配置的允许目录。
