#!/usr/bin/env python3
"""
图片水印工具
从图片的 EXIF 信息中提取拍摄时间作为水印，并添加到图片上
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import shutil

def get_exif_data(image_path):
    """从图片中提取 EXIF 数据"""
    try:
        with Image.open(image_path) as image:
            exif_data = image._getexif()
            if exif_data is not None:
                exif_dict = {}
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_dict[tag] = value
                return exif_dict
    except Exception as e:
        print(f"读取 {image_path} 的 EXIF 数据时出错: {e}")
    return None

def extract_datetime_from_exif(exif_data):
    """从 EXIF 数据中提取拍摄时间"""
    if not exif_data:
        return None
    
    # 尝试不同的日期时间字段
    datetime_fields = ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']
    
    for field in datetime_fields:
        if field in exif_data:
            datetime_str = exif_data[field]
            if datetime_str:
                # 提取年月日部分 (格式: YYYY:MM:DD HH:MM:SS)
                try:
                    date_part = datetime_str.split(' ')[0]  # 获取日期部分
                    year, month, day = date_part.split(':')
                    return f"{year}年{month}月{day}日"
                except:
                    continue
    
    return None

def get_image_files(directory):
    """获取目录下所有支持的图片文件"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.gif'}
    image_files = []
    
    for file_path in Path(directory).iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    return image_files

def get_font(size):
    """获取字体，如果系统字体不可用则使用默认字体"""
    try:
        # 尝试使用系统字体
        if sys.platform == "darwin":  # macOS
            font_path = "/System/Library/Fonts/Arial.ttf"
        elif sys.platform == "win32":  # Windows
            font_path = "C:/Windows/Fonts/arial.ttf"
        else:  # Linux
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    except:
        pass
    
    # 如果系统字体不可用，使用默认字体
    try:
        return ImageFont.load_default()
    except:
        return None

def add_watermark(image_path, watermark_text, font_size=24, color='white', position='bottom-right'):
    """为图片添加水印"""
    try:
        with Image.open(image_path) as image:
            # 创建绘图对象
            draw = ImageDraw.Draw(image)
            
            # 获取字体
            font = get_font(font_size)
            
            # 获取文本尺寸
            if font:
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            else:
                # 如果没有字体，估算文本尺寸
                text_width = len(watermark_text) * font_size // 2
                text_height = font_size
            
            # 计算水印位置
            img_width, img_height = image.size
            margin = 20
            
            if position == 'top-left':
                x, y = margin, margin
            elif position == 'top-right':
                x, y = img_width - text_width - margin, margin
            elif position == 'bottom-left':
                x, y = margin, img_height - text_height - margin
            elif position == 'bottom-right':
                x, y = img_width - text_width - margin, img_height - text_height - margin
            elif position == 'center':
                x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
            else:
                x, y = img_width - text_width - margin, img_height - text_height - margin
            
            # 绘制水印
            draw.text((x, y), watermark_text, fill=color, font=font)
            
            return image
            
    except Exception as e:
        print(f"处理图片 {image_path} 时出错: {e}")
        return None

def create_output_directory(original_dir):
    """创建输出目录"""
    output_dir = Path(original_dir) / f"{Path(original_dir).name}_watermark"
    output_dir.mkdir(exist_ok=True)
    return output_dir

def main():
    parser = argparse.ArgumentParser(description='为图片添加基于 EXIF 拍摄时间的水印')
    parser.add_argument('image_path', help='图片文件或目录路径')
    parser.add_argument('--font-size', type=int, default=24, help='字体大小 (默认: 24)')
    parser.add_argument('--color', default='white', help='水印颜色 (默认: white)')
    parser.add_argument('--position', choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'], 
                       default='bottom-right', help='水印位置 (默认: bottom-right)')
    
    args = parser.parse_args()
    
    image_path = Path(args.image_path)
    
    if not image_path.exists():
        print(f"错误: 路径 {image_path} 不存在")
        sys.exit(1)
    
    # 确定要处理的图片文件
    if image_path.is_file():
        image_files = [image_path]
        base_dir = image_path.parent
    else:
        image_files = get_image_files(image_path)
        base_dir = image_path
    
    if not image_files:
        print("错误: 未找到支持的图片文件")
        sys.exit(1)
    
    print(f"找到 {len(image_files)} 个图片文件")
    
    # 创建输出目录
    output_dir = create_output_directory(base_dir)
    print(f"输出目录: {output_dir}")
    
    processed_count = 0
    skipped_count = 0
    
    for image_file in image_files:
        print(f"处理: {image_file.name}")
        
        # 提取 EXIF 数据
        exif_data = get_exif_data(image_file)
        datetime_text = extract_datetime_from_exif(exif_data)
        
        if not datetime_text:
            print(f"  跳过: 无法从 EXIF 数据中提取拍摄时间")
            skipped_count += 1
            continue
        
        print(f"  拍摄时间: {datetime_text}")
        
        # 添加水印
        watermarked_image = add_watermark(
            image_file, 
            datetime_text, 
            args.font_size, 
            args.color, 
            args.position
        )
        
        if watermarked_image:
            # 保存到输出目录
            output_file = output_dir / image_file.name
            watermarked_image.save(output_file)
            print(f"  已保存: {output_file}")
            processed_count += 1
        else:
            print(f"  错误: 无法处理图片")
            skipped_count += 1
    
    print(f"\n处理完成!")
    print(f"成功处理: {processed_count} 个文件")
    print(f"跳过: {skipped_count} 个文件")

if __name__ == "__main__":
    main()
