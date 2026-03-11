---
name: clipboard
version: 1.0.0
title: 剪贴板
description: 读取和写入系统剪贴板内容
icon: "📋"
category: system
author: Ruixywie
tags: [clipboard, system, local]
skill_type: code
execution: local_agent
permissions: [clipboard]
source: official
tools:
  - name: read
    description: 读取当前剪贴板中的文本内容
  - name: write
    description: 将文本写入剪贴板
    parameters:
      text:
        type: string
        description: 要写入剪贴板的文本
        required: true
---

## Instructions

剪贴板工具在用户本地机器上执行，需要 Local Agent 运行。
read 返回当前剪贴板中的文本内容。
write 将指定文本复制到剪贴板，可在其他应用中粘贴使用。
