---
name: weather
version: 1.0.0
title: 天气查询
description: 使用 OpenWeather API 查询全球城市的实时天气信息
icon: "🌤️"
category: utility
author: Ruixywie
tags: [weather, utility]
skill_type: api
execution: server
permissions: [network]
source: official
base_url: https://api.openweathermap.org/data/2.5
auth:
  type: query_param
  param_name: appid
  env_key: OPENWEATHER_API_KEY
requires:
  env: [OPENWEATHER_API_KEY]
tools:
  - name: get_weather
    description: 查询指定城市的当前天气
    method: GET
    endpoint: /weather
    parameters:
      city:
        type: string
        description: 城市名称 (英文，如 Beijing, Tokyo, London)
        required: true
        mapping: q
      units:
        type: string
        description: 温度单位 (metric=摄氏度, imperial=华氏度)
        required: false
        default: metric
    extra_params:
      lang: zh_cn
    response_mapping:
      city: $.name
      country: $.sys.country
      temperature: $.main.temp
      feels_like: $.main.feels_like
      humidity: $.main.humidity
      description: $.weather.0.description
      wind_speed: $.wind.speed
    timeout: 15
---

## Instructions

使用 OpenWeather API 查询天气。城市名需要用英文，比如用 Beijing 而不是北京。
返回的温度默认是摄氏度。可以通过 units 参数切换到华氏度 (imperial)。
