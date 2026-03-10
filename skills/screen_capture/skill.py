"""
屏幕截图 Skill 实现

提供屏幕截图和屏幕查找功能。
"""

import base64
import io
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# 可选依赖
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False


def _check_dependencies() -> Optional[Dict[str, Any]]:
    """检查依赖是否满足"""
    if not HAS_PIL:
        return {"success": False, "error": "缺少依赖: pillow (pip install pillow)"}
    if not HAS_PYAUTOGUI:
        return {"success": False, "error": "缺少依赖: pyautogui (pip install pyautogui)"}
    return None


def _parse_region(region: str) -> Optional[Tuple[int, int, int, int]]:
    """
    解析区域参数

    Args:
        region: 区域字符串 'x,y,width,height' 或 'full'

    Returns:
        区域元组 (x, y, width, height) 或 None
    """
    if region.lower() == "full":
        return None

    try:
        parts = [int(p.strip()) for p in region.split(",")]
        if len(parts) != 4:
            return None
        return tuple(parts)
    except ValueError:
        return None


async def capture_screen(
    region: str = "full",
    save_path: str = None,
) -> Dict[str, Any]:
    """
    截取屏幕

    Args:
        region: 截取区域，格式：'x,y,width,height' 或 'full' 表示全屏
        save_path: 保存路径（可选，不指定则返回 base64）

    Returns:
        截图信息
    """
    error = _check_dependencies()
    if error:
        return error

    try:
        # 解析区域
        if region.lower() != "full":
            parsed_region = _parse_region(region)
            if parsed_region is None:
                return {
                    "success": False,
                    "error": f"无效的区域格式: {region}，应为 'x,y,width,height' 或 'full'",
                }
        else:
            parsed_region = None

        # 截取屏幕
        screenshot = pyautogui.screenshot(region=parsed_region)

        # 获取屏幕信息
        width, height = screenshot.size

        if save_path:
            # 保存到文件
            save_file = Path(save_path).expanduser().resolve()
            save_file.parent.mkdir(parents=True, exist_ok=True)
            screenshot.save(str(save_file))

            return {
                "success": True,
                "message": f"截图已保存到: {save_file}",
                "path": str(save_file),
                "width": width,
                "height": height,
            }
        else:
            # 缩放：最大边不超过 1280px，保持宽高比
            max_side = 1280
            if max(width, height) > max_side:
                scale = max_side / max(width, height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                screenshot = screenshot.resize(
                    (new_width, new_height), Image.LANCZOS
                )
            else:
                new_width, new_height = width, height

            # 压缩为 JPEG（体积从 5-10MB PNG 降到 100-300KB）
            if screenshot.mode == "RGBA":
                screenshot = screenshot.convert("RGB")
            buffer = io.BytesIO()
            screenshot.save(buffer, format="JPEG", quality=80)
            base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

            return {
                "success": True,
                "message": "截图成功",
                "base64": base64_data,
                "mime_type": "image/jpeg",
                "width": width,
                "height": height,
                "scaled_width": new_width,
                "scaled_height": new_height,
                "format": "JPEG",
            }

    except Exception as e:
        return {"success": False, "error": f"截图失败: {str(e)}"}


async def find_on_screen(
    target: str,
    confidence: float = 0.8,
) -> Dict[str, Any]:
    """
    在屏幕上查找目标图像

    Args:
        target: 目标图像路径
        confidence: 匹配置信度（0-1）

    Returns:
        查找结果
    """
    error = _check_dependencies()
    if error:
        return error

    try:
        # 验证目标图像路径
        target_path = Path(target).expanduser().resolve()

        if not target_path.exists():
            return {"success": False, "error": f"目标图像不存在: {target}"}

        # 查找图像
        try:
            location = pyautogui.locateOnScreen(
                str(target_path),
                confidence=confidence,
            )
        except pyautogui.ImageNotFoundException:
            location = None

        if location is None:
            return {
                "success": True,
                "found": False,
                "message": "未找到目标图像",
                "target": str(target_path),
            }

        # 获取中心点
        center = pyautogui.center(location)

        return {
            "success": True,
            "found": True,
            "message": "找到目标图像",
            "target": str(target_path),
            "location": {
                "x": location.left,
                "y": location.top,
                "width": location.width,
                "height": location.height,
            },
            "center": {
                "x": center.x,
                "y": center.y,
            },
        }

    except Exception as e:
        return {"success": False, "error": f"查找失败: {str(e)}"}


# 工具映射
TOOLS = {
    "capture_screen": capture_screen,
    "find_on_screen": find_on_screen,
}
