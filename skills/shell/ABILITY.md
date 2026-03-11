---
name: shell
version: 1.0.0
title: Shell 命令
description: 在用户本地机器上执行 Shell 命令（需要用户确认）
icon: "💻"
category: system
author: Ruixywie
tags: [shell, command, terminal, system, local]
requires: [local]
permissions: [shell]
source: official
---

## Instructions

Shell 命令能力包在用户本地机器上执行，需要 Local Agent 运行。
除非 Local Agent 以 --auto-confirm 模式启动，否则每条命令都需要用户确认才能执行。
命令有超时保护，默认 30 秒。
返回命令的标准输出、退出码和错误信息。
注意安全：避免执行破坏性命令（如 rm -rf、format 等）。

可用工具：`local_shell_exec`
