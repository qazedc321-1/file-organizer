"""
文件自动归类工具 - 将混乱的文件夹按文件类型自动整理到分类子文件夹中。
"""

import os
import shutil
import sys
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 文件分类规则：扩展名 -> 分类文件夹名
RULES = {
    # 图片
    ".jpg": "图片", ".jpeg": "图片", ".png": "图片", ".gif": "图片",
    ".bmp": "图片", ".svg": "图片", ".ico": "图片", ".webp": "图片",
    ".tif": "图片", ".tiff": "图片", ".heic": "图片", ".raw": "图片",

    # 文档
    ".pdf": "文档", ".doc": "文档", ".docx": "文档", ".xls": "文档",
    ".xlsx": "文档", ".ppt": "文档", ".pptx": "文档", ".txt": "文档",
    ".md": "文档", ".csv": "文档", ".json": "文档", ".xml": "文档",
    ".html": "文档", ".epub": "文档", ".mobi": "文档",

    # 视频
    ".mp4": "视频", ".avi": "视频", ".mkv": "视频", ".mov": "视频",
    ".wmv": "视频", ".flv": "视频", ".webm": "视频",

    # 音频
    ".mp3": "音频", ".wav": "音频", ".flac": "音频", ".aac": "音频",
    ".ogg": "音频", ".wma": "音频", ".m4a": "音频",

    # 压缩包
    ".zip": "压缩包", ".rar": "压缩包", ".7z": "压缩包", ".tar": "压缩包",
    ".gz": "压缩包", ".bz2": "压缩包", ".xz": "压缩包",

    # 代码/脚本
    ".py": "代码", ".js": "代码", ".ts": "代码", ".cpp": "代码",
    ".c": "代码", ".h": "代码", ".java": "代码", ".ino": "代码",
    ".css": "代码", ".sql": "代码", ".sh": "代码", ".bat": "代码",
    ".ps1": "代码",

    # 可执行/安装包
    ".exe": "程序包", ".msi": "程序包", ".apk": "程序包",
    ".dmg": "程序包", ".deb": "程序包", ".rpm": "程序包",

    # 3D/CAD
    ".stl": "3D模型", ".step": "3D模型", ".stp": "3D模型",
    ".iges": "3D模型", ".igs": "3D模型", ".sldprt": "3D模型",
    ".sldasm": "3D模型", ".obj": "3D模型", ".3mf": "3D模型",
}


def classify(file_name):
    """根据文件扩展名返回分类名，无法分类的返回 '其他'"""
    ext = Path(file_name).suffix.lower()
    return RULES.get(ext, "其他")


def scan_directory(path):
    """扫描目录中的所有文件，返回 {分类名: [文件名列表]} 的字典"""
    path = Path(path)
    if not path.exists() or not path.is_dir():
        print(f"错误：'{path}' 不是有效的目录")
        sys.exit(1)

    result = {}
    for item in path.iterdir():
        if item.is_file() and not item.name.startswith("."):
            category = classify(item.name)
            result.setdefault(category, []).append(item.name)
    return result


def preview(path, plan):
    """预览模式：显示将要执行的操作但不实际执行"""
    total = sum(len(files) for files in plan.values())
    if total == 0:
        print("没有需要整理的文件。")
        return False

    print(f"\n📂 目录: {path}")
    print(f"📄 共 {total} 个文件将被整理：\n")
    for category, files in sorted(plan.items()):
        print(f"  [{category}] ({len(files)} 个)")
        for f in sorted(files):
            print(f"    → {f}")
    return True


def execute(path, plan):
    """执行归类：创建子文件夹并移动文件"""
    path = Path(path)
    total = 0
    for category, files in plan.items():
        target_dir = path / category
        target_dir.mkdir(exist_ok=True)
        for f in files:
            src = path / f
            dst = target_dir / f
            shutil.move(str(src), str(dst))
            print(f"  移动: {f} → {category}/")
            total += 1
    print(f"\n✅ 完成！共整理 {total} 个文件。")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python organizer.py <目录路径>       整理指定目录")
        print("  python organizer.py <目录路径> --dry  预览模式（不实际执行）")
        print("\n示例:")
        print("  python organizer.py C:\\Users\\emo\\Downloads")
        print("  python organizer.py C:\\Users\\emo\\Downloads --dry")
        sys.exit(1)

    target = sys.argv[1]
    dry_run = "--dry" in sys.argv

    plan = scan_directory(target)

    if dry_run:
        preview(target, plan)
    else:
        if not preview(target, plan):
            return
        print("\n按 Enter 确认执行，Ctrl+C 取消...", end="")
        try:
            input()
        except KeyboardInterrupt:
            print("\n取消操作。")
            return
        execute(target, plan)


if __name__ == "__main__":
    main()
