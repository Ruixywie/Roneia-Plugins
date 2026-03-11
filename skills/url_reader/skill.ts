/**
 * URL Reader - Code Skill
 * Fetches web pages and extracts plain text content
 */

async function read_url(args: { url: string; max_length?: number }) {
  const { url, max_length = 5000 } = args

  try {
    // Validate URL
    const parsedUrl = new URL(url)
    if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
      return { success: false, error: 'Only http and https URLs are supported' }
    }

    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; Roneia/2.0; +https://github.com/Ruixywie/roneia)',
        'Accept': 'text/html,application/xhtml+xml,text/plain,*/*',
      },
    })

    if (!response.ok) {
      return { success: false, error: `HTTP ${response.status}: ${response.statusText}` }
    }

    const contentType = response.headers.get('content-type') || ''
    const rawText = await response.text()

    let text: string
    if (contentType.includes('text/html') || contentType.includes('application/xhtml')) {
      text = extractTextFromHtml(rawText)
    } else {
      // Plain text or other formats
      text = rawText
    }

    // Trim to max length
    if (text.length > max_length) {
      text = text.substring(0, max_length) + '\n\n[... 内容已截断，共 ' + rawText.length + ' 字符]'
    }

    return {
      success: true,
      result: {
        url,
        content_type: contentType,
        length: text.length,
        text,
      },
    }
  } catch (err) {
    return { success: false, error: String(err) }
  }
}

function extractTextFromHtml(html: string): string {
  // Remove script and style blocks
  let text = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, '')
    .replace(/<nav[\s\S]*?<\/nav>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '')
    .replace(/<header[\s\S]*?<\/header>/gi, '')

  // Convert common elements to text with spacing
  text = text
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<\/div>/gi, '\n')
    .replace(/<\/h[1-6]>/gi, '\n\n')
    .replace(/<\/li>/gi, '\n')
    .replace(/<li[^>]*>/gi, '- ')
    .replace(/<\/tr>/gi, '\n')
    .replace(/<td[^>]*>/gi, '\t')

  // Remove all remaining HTML tags
  text = text.replace(/<[^>]*>/g, '')

  // Decode common HTML entities
  text = text
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(parseInt(code)))

  // Clean up whitespace
  text = text
    .replace(/[ \t]+/g, ' ')
    .replace(/\n\s*\n\s*\n/g, '\n\n')
    .trim()

  return text
}

module.exports = {
  TOOLS: { read_url },
}
