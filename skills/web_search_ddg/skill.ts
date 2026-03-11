/**
 * DuckDuckGo Search - Code Skill
 * Uses DuckDuckGo HTML API to search the web without any API key
 */

async function search(args: { query: string; max_results?: number }) {
  const { query, max_results = 5 } = args
  const maxResults = Math.min(Math.max(max_results, 1), 10)

  try {
    const url = new URL('https://html.duckduckgo.com/html/')
    const body = new URLSearchParams({ q: query, kl: '' })

    const response = await fetch(url.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      },
      body: body.toString(),
    })

    if (!response.ok) {
      return { success: false, error: `DuckDuckGo returned status ${response.status}` }
    }

    const html = await response.text()

    // Parse search results from HTML
    const results: { title: string; url: string; snippet: string }[] = []
    const resultPattern = /<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>[\s\S]*?<a[^>]*class="result__snippet"[^>]*>([\s\S]*?)<\/a>/g

    let match
    while ((match = resultPattern.exec(html)) !== null && results.length < maxResults) {
      const rawUrl = match[1] || ''
      const title = (match[2] || '').replace(/<[^>]*>/g, '').trim()
      const snippet = (match[3] || '').replace(/<[^>]*>/g, '').trim()

      // DuckDuckGo wraps URLs in a redirect; extract the actual URL
      let actualUrl = rawUrl
      const udParam = new URLSearchParams(rawUrl.split('?')[1] || '')
      if (udParam.has('uddg')) {
        actualUrl = decodeURIComponent(udParam.get('uddg')!)
      }

      if (title && snippet) {
        results.push({ title, url: actualUrl, snippet })
      }
    }

    // Fallback: simpler pattern for newer HTML
    if (results.length === 0) {
      const simplePattern = /<h2[^>]*class="[^"]*result__title[^"]*"[^>]*>[\s\S]*?<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>[\s\S]*?<a[^>]*class="[^"]*result__snippet[^"]*"[^>]*>([\s\S]*?)<\/a>/g
      while ((match = simplePattern.exec(html)) !== null && results.length < maxResults) {
        const rawUrl = match[1] || ''
        const title = (match[2] || '').replace(/<[^>]*>/g, '').trim()
        const snippet = (match[3] || '').replace(/<[^>]*>/g, '').trim()
        if (title) {
          results.push({ title, url: rawUrl, snippet })
        }
      }
    }

    return {
      success: true,
      result: {
        query,
        results,
        total: results.length,
      },
    }
  } catch (err) {
    return { success: false, error: String(err) }
  }
}

module.exports = {
  TOOLS: { search },
}
