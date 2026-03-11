---
name: url_reader
version: 1.0.0
title: 网页阅读器
description: 读取网页内容并提取纯文本，支持限制返回长度
icon: "📄"
category: utility
author: Ruixywie
tags: [web, reader, utility]
skill_type: code
execution: server
permissions: [network]
source: official
tools:
  - name: read_url
    description: 读取指定 URL 的网页内容，返回纯文本
    parameters:
      url:
        type: string
        description: 要读取的网页 URL
        required: true
      max_length:
        type: integer
        description: 返回文本的最大字符数
        required: false
        default: 5000
---

## Instructions

网页阅读器工具可以获取任意 URL 的内容并提取纯文本。
适合用于阅读文章、查看文档、获取网页信息等场景。
自动去除 HTML 标签和脚本，只保留有意义的文本内容。
