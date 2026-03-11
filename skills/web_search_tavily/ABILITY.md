---
name: web_search_tavily
version: 1.0.0
title: Tavily 网络搜索
description: 使用 Tavily API 搜索互联网，获取最新信息和网页内容摘要
icon: "🔍"
category: search
author: Ruixywie
tags: [search, web, tavily]
permissions: [network]
source: official
requires_env: [TAVILY_API_KEY]
api:
  base_url: https://api.tavily.com
  auth:
    type: body_param
    param_name: api_key
    env_key: TAVILY_API_KEY
tools:
  - name: search
    description: 搜索互联网获取最新信息
    method: POST
    endpoint: /search
    parameters:
      query:
        type: string
        description: 搜索关键词
        required: true
      search_depth:
        type: string
        description: 搜索深度 (basic 或 advanced)
        required: false
        default: basic
      max_results:
        type: integer
        description: 最大返回结果数
        required: false
        default: 5
    extra_params:
      include_answer: true
    response_mapping:
      answer: $.answer
      results: $.results
    timeout: 30
---

## Instructions

Tavily 是一个专为 AI Agent 设计的搜索 API，能返回结构化的搜索结果和直接回答。
使用 `search` 工具来搜索互联网上的最新信息。
搜索结果包含 `answer`（直接回答）和 `results`（搜索结果列表）。
对于需要深度分析的查询，可以设置 `search_depth` 为 `advanced`。
