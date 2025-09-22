# 图片水印工具

一个基于 Python 的命令行工具，可以从图片的 EXIF 信息中提取拍摄时间，并将其作为水印添加到图片上。

## 功能特性

- 📸 自动从图片 EXIF 数据中提取拍摄时间
- 🎨 支持自定义水印字体大小、颜色和位置
- 📁 批量处理目录下的所有图片文件
- 💾 自动创建输出目录保存处理后的图片
- 🖼️ 支持多种图片格式 (JPG, PNG, TIFF, BMP, GIF)

## 安装依赖

### 方法一：使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 方法二：直接安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# 激活虚拟环境（如果使用虚拟环境）
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 处理单个图片文件
python watermark_tool.py /path/to/image.jpg

# 处理整个目录下的所有图片
python watermark_tool.py /path/to/images/
```

### 高级选项

```bash
# 激活虚拟环境（如果使用虚拟环境）
source venv/bin/activate

python watermark_tool.py /path/to/images/ \
    --font-size 32 \
    --color red \
    --position center
```

### 参数说明

- `image_path`: 图片文件或目录路径（必需）
- `--font-size`: 字体大小，默认 24
- `--color`: 水印颜色，默认 white
- `--position`: 水印位置，可选值：
  - `top-left`: 左上角
  - `top-right`: 右上角
  - `bottom-left`: 左下角
  - `bottom-right`: 右下角（默认）
  - `center`: 居中

## 输出

程序会在原目录下创建一个名为 `原目录名_watermark` 的子目录，所有处理后的图片都会保存在这个目录中。

例如：
- 输入目录：`/photos/vacation/`
- 输出目录：`/photos/vacation/vacation_watermark/`

## 示例

```bash
# 激活虚拟环境
source venv/bin/activate

# 处理 vacation 目录下的所有图片，使用红色水印，字体大小 30，位置在右下角
python watermark_tool.py /Users/john/Photos/vacation/ --font-size 30 --color red --position bottom-right
```

## 注意事项

1. 程序会尝试从图片的 EXIF 数据中提取拍摄时间，如果图片没有 EXIF 数据或拍摄时间信息，该图片将被跳过
2. 支持的图片格式：JPG, JPEG, PNG, TIFF, TIF, BMP, GIF
3. 程序会自动尝试使用系统字体，如果系统字体不可用，会使用默认字体
4. 水印文本格式为：`YYYY年MM月DD日`

## 错误处理

- 如果图片文件损坏或无法读取，程序会跳过该文件并继续处理其他文件
- 如果无法提取 EXIF 数据，程序会跳过该文件
- 所有错误信息都会在控制台显示

## 系统要求

- Python 3.6+
- Pillow 库 (PIL)
