"""
本地文件 Skill 实现

提供文件和文件夹的打开、读取、搜索功能。
"""

import os
import glob
import subprocess
import platform
from pathlib import Path
from typing import Any, Dict


async def open_file(path: str) -> Dict[str, Any]:
    """
    使用系统默认程序打开文件或文件夹

    Args:
        path: 文件或文件夹的路径

    Returns:
        操作结果
    """
    try:
        file_path = Path(path).expanduser().resolve()

        if not file_path.exists():
            return {"success": False, "error": f"路径不存在: {path}"}

        system = platform.system()

        if system == "Windows":
            os.startfile(str(file_path))
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(file_path)], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(file_path)], check=True)

        return {
            "success": True,
            "message": f"已打开: {file_path}",
            "path": str(file_path),
            "is_directory": file_path.is_dir(),
        }

    except Exception as e:
        return {"success": False, "error": f"打开失败: {str(e)}"}


async def read_file(
    path: str,
    encoding: str = "utf-8",
    max_lines: int = 100,
) -> Dict[str, Any]:
    """
    读取文件内容

    Args:
        path: 文件路径
        encoding: 文件编码
        max_lines: 最大读取行数（0 表示全部）

    Returns:
        文件内容
    """
    try:
        file_path = Path(path).expanduser().resolve()

        if not file_path.exists():
            return {"success": False, "error": f"文件不存在: {path}"}

        if file_path.is_dir():
            return {"success": False, "error": f"路径是目录，不是文件: {path}"}

        # 检查文件大小
        file_size = file_path.stat().st_size
        if file_size > 10 * 1024 * 1024:  # 10MB
            return {"success": False, "error": f"文件太大 ({file_size} bytes)，最大支持 10MB"}

        # 读取文件
        with open(file_path, "r", encoding=encoding) as f:
            if max_lines > 0:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    lines.append(line)
                content = "".join(lines)
                truncated = i >= max_lines
            else:
                content = f.read()
                truncated = False

        return {
            "success": True,
            "content": content,
            "path": str(file_path),
            "size": file_size,
            "lines": len(content.splitlines()),
            "truncated": truncated,
        }

    except UnicodeDecodeError:
        return {"success": False, "error": f"无法以 {encoding} 编码读取文件，可能是二进制文件"}
    except Exception as e:
        return {"success": False, "error": f"读取失败: {str(e)}"}


async def search_files(
    pattern: str,
    directory: str = ".",
    recursive: bool = True,
    max_results: int = 50,
) -> Dict[str, Any]:
    """
    搜索文件

    Args:
        pattern: 搜索模式（支持 * 和 ? 通配符）
        directory: 搜索目录
        recursive: 是否递归搜索子目录
        max_results: 最大结果数

    Returns:
        匹配的文件列表
    """
    try:
        search_dir = Path(directory).expanduser().resolve()

        if not search_dir.exists():
            return {"success": False, "error": f"目录不存在: {directory}"}

        if not search_dir.is_dir():
            return {"success": False, "error": f"路径不是目录: {directory}"}

        # 构建搜索模式
        if recursive:
            search_pattern = str(search_dir / "**" / pattern)
        else:
            search_pattern = str(search_dir / pattern)

        # 搜索文件
        matches = []
        for match in glob.iglob(search_pattern, recursive=recursive):
            match_path = Path(match)
            matches.append({
                "path": str(match_path),
                "name": match_path.name,
                "is_directory": match_path.is_dir(),
                "size": match_path.stat().st_size if match_path.is_file() else 0,
            })

            if len(matches) >= max_results:
                break

        return {
            "success": True,
            "matches": matches,
            "count": len(matches),
            "search_directory": str(search_dir),
            "pattern": pattern,
            "truncated": len(matches) >= max_results,
        }

    except Exception as e:
        return {"success": False, "error": f"搜索失败: {str(e)}"}


# 工具映射
TOOLS = {
    "open_file": open_file,
    "read_file": read_file,
    "search_files": search_files,
}
