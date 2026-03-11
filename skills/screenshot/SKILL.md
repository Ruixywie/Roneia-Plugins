---
name: screenshot
version: 1.0.0
title: 屏幕截图与识别
description: 截取用户屏幕画面并支持 AI 视觉理解分析
icon: "📸"
category: system
author: Ruixywie
tags: [screenshot, screen, vision, system, local]
skill_type: code
execution: local_agent
permissions: [screenshot]
source: official
tools:
  - name: capture_screen
    description: 截取屏幕画面，AI 可以直接看到并分析截图内容
    output_type: image
    parameters:
      display:
        type: integer
        description: 显示器编号（从 0 开始，默认主显示器）
        required: false
        default: 0
  - name: list_displays
    description: 列出所有可用的显示器及其分辨率信息
---

## Instructions

屏幕截图工具在用户本地机器上执行，需要 Local Agent 运行。
capture_screen 截取完整画面并自动传给 AI 进行视觉理解。
