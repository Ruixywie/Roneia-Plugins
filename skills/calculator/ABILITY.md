---
name: calculator
version: 1.0.0
title: 计算器
description: 安全地计算数学表达式，支持基本运算和常见数学函数
icon: "🧮"
category: utility
author: Ruixywie
tags: [math, calculator, utility]
permissions: []
source: official
tools:
  - name: calculate
    description: 计算数学表达式
    parameters:
      expression:
        type: string
        description: "数学表达式，如 2+3*4, sqrt(16), sin(3.14), 2**10"
        required: true
---

## Instructions

计算器工具可以安全地计算数学表达式。支持的操作包括：
- 基本运算：加(+)、减(-)、乘(*)、除(/)、取余(%)、幂(**)
- 数学函数：sqrt、abs、sin、cos、tan、log、log2、log10、ceil、floor、round
- 常量：PI、E
- 括号嵌套

## Implementation

```typescript
const MATH_FUNCS: Record<string, (x: number) => number> = {
  sqrt: Math.sqrt,
  abs: Math.abs,
  sin: Math.sin,
  cos: Math.cos,
  tan: Math.tan,
  log: Math.log,
  log2: Math.log2,
  log10: Math.log10,
  ceil: Math.ceil,
  floor: Math.floor,
  round: Math.round,
  exp: Math.exp,
}

const CONSTANTS: Record<string, number> = {
  PI: Math.PI,
  E: Math.E,
}

function tokenize(expr: string): string[] {
  const tokens: string[] = []
  let i = 0
  while (i < expr.length) {
    if (expr[i] === ' ') { i++; continue }
    if ('+-*/%()'.includes(expr[i])) {
      if (expr[i] === '*' && expr[i+1] === '*') {
        tokens.push('**')
        i += 2
      } else {
        tokens.push(expr[i])
        i++
      }
    } else if (/[0-9.]/.test(expr[i])) {
      let num = ''
      while (i < expr.length && /[0-9.]/.test(expr[i])) { num += expr[i]; i++ }
      tokens.push(num)
    } else if (/[a-zA-Z_]/.test(expr[i])) {
      let name = ''
      while (i < expr.length && /[a-zA-Z0-9_]/.test(expr[i])) { name += expr[i]; i++ }
      tokens.push(name)
    } else {
      throw new Error('Unexpected character: ' + expr[i])
    }
  }
  return tokens
}

function parse(tokens: string[]): number {
  let pos = 0

  function parseExpr(): number {
    let left = parseTerm()
    while (pos < tokens.length && (tokens[pos] === '+' || tokens[pos] === '-')) {
      const op = tokens[pos]; pos++
      const right = parseTerm()
      left = op === '+' ? left + right : left - right
    }
    return left
  }

  function parseTerm(): number {
    let left = parsePower()
    while (pos < tokens.length && (tokens[pos] === '*' || tokens[pos] === '/' || tokens[pos] === '%')) {
      const op = tokens[pos]; pos++
      const right = parsePower()
      if (op === '*') left *= right
      else if (op === '/') { if (right === 0) throw new Error('Division by zero'); left /= right }
      else left %= right
    }
    return left
  }

  function parsePower(): number {
    let base = parseUnary()
    while (pos < tokens.length && tokens[pos] === '**') {
      pos++
      const exp = parseUnary()
      base = Math.pow(base, exp)
    }
    return base
  }

  function parseUnary(): number {
    if (tokens[pos] === '-') { pos++; return -parseAtom() }
    if (tokens[pos] === '+') { pos++; return parseAtom() }
    return parseAtom()
  }

  function parseAtom(): number {
    const token = tokens[pos]
    if (!token) throw new Error('Unexpected end of expression')

    // Number
    if (/^[0-9.]/.test(token)) {
      pos++
      return parseFloat(token)
    }

    // Parenthesized expression
    if (token === '(') {
      pos++
      const val = parseExpr()
      if (tokens[pos] !== ')') throw new Error('Missing closing parenthesis')
      pos++
      return val
    }

    // Function call or constant
    if (/^[a-zA-Z_]/.test(token)) {
      pos++
      if (CONSTANTS[token] !== undefined) return CONSTANTS[token]
      const fn = MATH_FUNCS[token]
      if (fn) {
        if (tokens[pos] !== '(') throw new Error('Expected ( after function ' + token)
        pos++
        const arg = parseExpr()
        if (tokens[pos] !== ')') throw new Error('Missing closing parenthesis')
        pos++
        return fn(arg)
      }
      throw new Error('Unknown identifier: ' + token)
    }

    throw new Error('Unexpected token: ' + token)
  }

  const result = parseExpr()
  if (pos < tokens.length) throw new Error('Unexpected token after expression: ' + tokens[pos])
  return result
}

async function calculate(args: { expression: string }) {
  try {
    const tokens = tokenize(args.expression)
    const result = parse(tokens)

    if (!isFinite(result)) {
      return { success: true, result: { expression: args.expression, result: String(result) } }
    }

    return {
      success: true,
      result: {
        expression: args.expression,
        result: Number.isInteger(result) ? result : parseFloat(result.toFixed(10)),
      },
    }
  } catch (err) {
    return { success: false, error: String(err) }
  }
}

module.exports = {
  TOOLS: { calculate },
}
```
