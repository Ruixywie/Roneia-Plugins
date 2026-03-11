---
name: time_date
version: 1.0.0
title: 时间日期
description: 获取当前日期和时间，支持不同时区
icon: "🕐"
category: utility
author: Ruixywie
tags: [time, date, utility]
skill_type: code
execution: server
permissions: []
source: official
tools:
  - name: get_current_time
    description: 获取当前日期和时间
    parameters:
      timezone:
        type: string
        description: "IANA 时区名称，如 Asia/Shanghai, America/New_York, Europe/London"
        required: false
        default: Asia/Shanghai
---

## Instructions

时间日期工具返回指定时区的当前日期和时间。
默认返回北京时间 (Asia/Shanghai)。用户可以指定任何 IANA 时区。

## Implementation

```typescript
async function get_current_time(args: { timezone?: string }) {
  const tz = args.timezone || 'Asia/Shanghai'

  try {
    const now = new Date()

    const formatter = new Intl.DateTimeFormat('zh-CN', {
      timeZone: tz,
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      weekday: 'long',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    })

    const parts = formatter.formatToParts(now)
    const get = (type: string) => parts.find(p => p.type === type)?.value || ''

    const dateStr = `${get('year')}-${get('month')}-${get('day')}`
    const timeStr = `${get('hour')}:${get('minute')}:${get('second')}`
    const weekday = get('weekday')

    return {
      success: true,
      result: {
        timezone: tz,
        date: dateStr,
        time: timeStr,
        weekday,
        formatted: `${dateStr} ${weekday} ${timeStr}`,
        timestamp: now.getTime(),
        iso: now.toISOString(),
      },
    }
  } catch (err) {
    return { success: false, error: `Invalid timezone: ${tz}. ${String(err)}` }
  }
}

module.exports = {
  TOOLS: { get_current_time },
}
```
