---
name: shell
version: 1.0.0
title: Shell 命令
description: 在用户本地机器上执行 Shell 命令（需要用户确认）
icon: "💻"
category: system
author: Ruixywie
tags: [shell, command, terminal, system, local]
skill_type: code
execution: local_agent
permissions: [shell]
source: official
tools:
  - name: execute
    description: 执行一条 Shell 命令（Windows 用 cmd /c，Linux/macOS 用 sh -c）
    parameters:
      command:
        type: string
        description: 要执行的命令
        required: true
      timeout:
        type: number
        description: 超时时间（秒），默认 30 秒
        required: false
        default: 30
---

## Instructions

Shell 命令工具在用户本地机器上执行，需要 Local Agent 运行。
除非 Local Agent 以 --auto-confirm 模式启动，否则每条命令都需要用户确认才能执行。
命令有超时保护，默认 30 秒。
返回命令的标准输出、退出码和错误信息。
注意安全：避免执行破坏性命令（如 rm -rf、format 等）。
