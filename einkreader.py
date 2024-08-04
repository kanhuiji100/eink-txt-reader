from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def text_to_image(input_file, output_folder, font_path, font_size=12, image_size=(400, 300)):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    font = ImageFont.truetype(font_path, font_size)
    paragraphs = text.split('\n')

    images = []
    current_image = Image.new('RGB', image_size, color='white')
    draw = ImageDraw.Draw(current_image)
    y_text = 0
    page_number = 1

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_lines = sum(len(textwrap.wrap(paragraph, width=33)) for paragraph in paragraphs)
    lines_processed = 0

    for paragraph in paragraphs:
        lines = textwrap.wrap(paragraph, width=33)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if y_text + height > image_size[1] - height:  
                footer_text = f'Page {page_number} - {int((lines_processed / total_lines) * 100)}%'
                draw.text((0, image_size[1] - height), footer_text, font=font, fill='black')
                images.append(current_image)
                current_image = Image.new('RGB', image_size, color='white')
                draw = ImageDraw.Draw(current_image)
                y_text = 0
                page_number += 1

            draw.text((0, y_text), line, font=font, fill='black')
            y_text += height
            lines_processed += 1

        y_text += height

    for i, img in enumerate(images):
        output_path = os.path.join(output_folder, f'page_{i+1}.bmp')
        img.save(output_path)
        print(f'Saved: {output_path}')

text_to_image('C:\\Users\\Plane\\Desktop\\eink\\input2.txt', 'C:\\Users\\Plane\\Desktop\\eink\\output_folder', 'C:\\Users\\Plane\\Desktop\\eink\\simsun.ttc')
