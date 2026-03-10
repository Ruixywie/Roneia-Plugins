"""
网页搜索 Skill 实现

提供网页搜索和内容获取功能。
支持 Tavily Search（主力）和 DuckDuckGo（降级方案）双引擎。
"""

import asyncio
import logging
from typing import Any, Dict
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# 可选依赖 - Tavily
try:
    from tavily import TavilyClient
    HAS_TAVILY = True
except ImportError:
    HAS_TAVILY = False

# 可选依赖 - DuckDuckGo
try:
    from ddgs import DDGS
    HAS_DDGS = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        HAS_DDGS = True
    except ImportError:
        HAS_DDGS = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


# ============================================================================
# 模块级搜索配置（由 main.py 在启用 skill 时注入）
# ============================================================================

_search_config: Dict[str, Any] = {}


def configure(config: Dict[str, Any]) -> None:
    """注入 Server 下发的搜索配置"""
    global _search_config
    _search_config = config
    logger.info(f"Search config loaded: provider={config.get('provider', 'auto')}, "
                f"tavily_key={'configured' if config.get('tavily_api_key') else 'not set'}")


# ============================================================================
# Tavily 搜索
# ============================================================================

async def _search_tavily(query: str, num_results: int, api_key: str) -> Dict[str, Any]:
    """使用 Tavily API 搜索"""
    client = TavilyClient(api_key=api_key)
    response = await asyncio.to_thread(
        client.search,
        query=query,
        max_results=num_results,
        search_depth=_search_config.get("tavily_search_depth", "basic"),
        include_answer=_search_config.get("tavily_include_answer", True),
    )
    results = []
    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": item.get("content", ""),
        })
    return {
        "success": True,
        "results": results,
        "query": query,
        "count": len(results),
        "answer": response.get("answer", ""),
        "provider": "tavily",
    }


# ============================================================================
# DuckDuckGo 搜索
# ============================================================================

async def _search_duckduckgo(query: str, num_results: int) -> Dict[str, Any]:
    """使用 DuckDuckGo 搜索"""
    if not HAS_DDGS:
        return {"success": False, "error": "缺少依赖: ddgs (pip install ddgs)"}

    try:
        raw_results = await asyncio.to_thread(
            lambda: DDGS().text(query, region="wt-wt", max_results=num_results)
        )

        results = []
        for item in raw_results:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", ""),
            })

        return {
            "success": True,
            "results": results,
            "query": query,
            "count": len(results),
            "provider": "duckduckgo",
        }

    except Exception as e:
        return {"success": False, "error": f"搜索失败: {str(e)}"}


# ============================================================================
# 搜索入口（双引擎策略）
# ============================================================================

async def search(
    query: str,
    num_results: int = 5,
) -> Dict[str, Any]:
    """
    使用搜索引擎搜索信息

    Args:
        query: 搜索关键词
        num_results: 返回结果数量

    Returns:
        搜索结果列表
    """
    api_key = _search_config.get("tavily_api_key", "")
    provider = _search_config.get("provider", "auto")

    # 决定使用哪个引擎
    use_tavily = (
        HAS_TAVILY and api_key and provider in ("tavily", "auto")
    )

    if use_tavily:
        try:
            return await _search_tavily(query, num_results, api_key)
        except Exception as e:
            logger.warning(f"Tavily search failed, falling back to DuckDuckGo: {e}")
            # 降级到 DuckDuckGo

    # 配置了 tavily 但未安装库时给出提示
    if api_key and not HAS_TAVILY and provider in ("tavily", "auto"):
        logger.warning("tavily-python not installed, using DuckDuckGo. "
                        "Install with: pip install tavily-python")

    return await _search_duckduckgo(query, num_results)


async def fetch_page(
    url: str,
    extract_text: bool = True,
    max_length: int = 5000,
) -> Dict[str, Any]:
    """
    获取网页内容

    Args:
        url: 网页 URL
        extract_text: 是否只提取文本
        max_length: 最大内容长度

    Returns:
        网页内容
    """
    if not HAS_REQUESTS:
        return {"success": False, "error": "缺少依赖: requests (pip install requests)"}

    try:
        # 验证 URL
        parsed = urlparse(url)
        if not parsed.scheme:
            url = "https://" + url
            parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return {"success": False, "error": f"不支持的协议: {parsed.scheme}"}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if "text/html" in content_type:
            if not HAS_BS4:
                # 没有 bs4 时返回原始文本
                content = response.text[:max_length]
                return {
                    "success": True,
                    "url": url,
                    "title": "",
                    "content": content,
                    "length": len(content),
                    "content_type": content_type,
                }

            soup = BeautifulSoup(response.text, "html.parser")

            # 获取标题
            title = ""
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True)

            if extract_text:
                # 移除脚本和样式
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                # 提取文本
                text = soup.get_text(separator="\n", strip=True)

                # 清理多余空行
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                content = "\n".join(lines)
            else:
                content = response.text

            # 截断
            if len(content) > max_length:
                content = content[:max_length] + "...[已截断]"

            return {
                "success": True,
                "url": url,
                "title": title,
                "content": content,
                "length": len(content),
                "content_type": content_type,
            }

        else:
            return {"success": False, "error": f"不支持的内容类型: {content_type}"}

    except requests.Timeout:
        return {"success": False, "error": "请求超时"}
    except requests.HTTPError as e:
        return {"success": False, "error": f"HTTP 错误: {e.response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"获取失败: {str(e)}"}


# 工具映射
TOOLS = {
    "search": search,
    "fetch_page": fetch_page,
}
