---
name: app_monitor
version: 1.0.0
title: 应用窗口监控
description: 检测当前活动的应用窗口标题
icon: "🪟"
category: system
author: Ruixywie
tags: [window, application, monitor, system, local]
skill_type: code
execution: local_agent
permissions: [app_monitor]
source: official
tools:
  - name: get_active
    description: 获取当前活动窗口（前台窗口）的标题
---

## Instructions

应用窗口监控工具在用户本地机器上执行，需要 Local Agent 运行。
get_active 返回当前前台窗口的标题，可用于了解用户正在使用什么应用。
Windows 使用 Win32 API，Linux 使用 xdotool。
