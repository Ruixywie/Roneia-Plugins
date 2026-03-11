---
name: clipboard
version: 1.0.0
title: 剪贴板
description: 读取和写入系统剪贴板内容
icon: "📋"
category: system
author: Ruixywie
tags: [clipboard, system, local]
requires: [local]
permissions: [clipboard]
source: official
---

## Instructions

剪贴板能力包在用户本地机器上执行，需要 Local Agent 运行。
`local_clipboard_read` 返回当前剪贴板中的文本内容。
`local_clipboard_write` 将指定文本复制到剪贴板，可在其他应用中粘贴使用。
