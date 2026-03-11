---
name: app_monitor
version: 1.0.0
title: 应用窗口监控
description: 检测当前活动的应用窗口标题
icon: "🪟"
category: system
author: Ruixywie
tags: [window, application, monitor, system, local]
requires: [local]
permissions: [app_monitor]
source: official
---

## Instructions

应用窗口监控能力包在用户本地机器上执行，需要 Local Agent 运行。
`local_app_active` 返回当前前台窗口的标题，可用于了解用户正在使用什么应用。
Windows 使用 Win32 API，Linux 使用 xdotool。
