# File Organizer

一键整理混乱的文件夹——按文件类型自动归类到子文件夹中。

## 功能

- 支持 70+ 种文件格式，归类为：图片、文档、视频、音频、压缩包、代码、程序包、3D模型等
- 预览模式（`--dry`）：先看效果再决定是否执行
- 安全确认：执行前需手动确认

## 快速开始

```bash
# 预览将要整理的文件
python organizer.py C:\Users\emo\Downloads --dry

# 确认无误后执行整理
python organizer.py C:\Users\emo\Downloads
```

## 分类规则

| 分类 | 包含格式 |
|------|---------|
| 图片 | jpg, png, gif, svg, bmp, webp, raw... |
| 文档 | pdf, doc, xlsx, ppt, txt, csv, json... |
| 视频 | mp4, avi, mkv, mov, webm... |
| 音频 | mp3, wav, flac, aac... |
| 压缩包 | zip, rar, 7z, tar.gz... |
| 代码 | py, js, ts, cpp, java, ino... |
| 3D模型 | stl, step, sldprt, obj... |

## 自定义分类

编辑 `organizer.py` 中的 `RULES` 字典，添加你自己的扩展名和分类即可。
