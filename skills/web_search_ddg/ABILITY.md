---
name: web_search_ddg
version: 1.0.0
title: DuckDuckGo 搜索
description: 使用 DuckDuckGo 搜索互联网，无需 API Key，完全免费
icon: "🦆"
category: search
author: Ruixywie
tags: [search, web, free]
permissions: [network]
source: official
tools:
  - name: search
    description: 使用 DuckDuckGo 搜索互联网
    parameters:
      query:
        type: string
        description: 搜索关键词
        required: true
      max_results:
        type: integer
        description: 最大返回结果数 (1-10)
        required: false
        default: 5
---

## Instructions

DuckDuckGo 搜索是一个免费的搜索工具，无需任何 API Key。
适合作为 Tavily 搜索的备选方案。搜索结果包含标题、摘要和链接。
