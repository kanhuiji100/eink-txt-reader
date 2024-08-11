from PIL import Image, ImageDraw, ImageFont
import os

def text_to_image(input_file, output_folder, font_path=None, font_size=12, image_size=(400, 300), paragraph_spacing=10):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    paragraphs = text.split('\n')

    images = []
    current_image = Image.new('RGB', image_size, color='white')
    draw = ImageDraw.Draw(current_image)
    y_text = 0
    page_number = 1

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_lines = sum(len(paragraph) for paragraph in paragraphs)
    lines_processed = 0

    for paragraph in paragraphs:
        line = ''
        for char in paragraph:
            test_line = f'{line}{char}'
            width = draw.textlength(test_line, font=font)
            if width <= image_size[0]:
                line = test_line
            else:
                bbox = draw.textbbox((0, 0), line, font=font)
                _, _, _, height = bbox
                if y_text + height > image_size[1] - height:
                    footer_text = f'Page {page_number} of {page_number} - {int((lines_processed / total_lines) * 100)}%'
                    draw.text((0, image_size[1] - height), footer_text, font=font, fill='black')
                    images.append(current_image)
                    current_image = Image.new('RGB', image_size, color='white')
                    draw = ImageDraw.Draw(current_image)
                    y_text = 0
                    page_number += 1

                draw.text((0, y_text), line, font=font, fill='black')
                y_text += height
                lines_processed += len(line)
                line = char

        if line:
            bbox = draw.textbbox((0, 0), line, font=font)
            _, _, _, height = bbox
            if y_text + height > image_size[1] - height:
                footer_text = f'Page {page_number} of {page_number} - {int((lines_processed / total_lines) * 100)}%'
                draw.text((0, image_size[1] - height), footer_text, font=font, fill='black')
                images.append(current_image)
                current_image = Image.new('RGB', image_size, color='white')
                draw = ImageDraw.Draw(current_image)
                y_text = 0
                page_number += 1

            draw.text((0, y_text), line, font=font, fill='black')
            y_text += height
            lines_processed += len(line)

        y_text += paragraph_spacing

    footer_text = f'Page {page_number} of {page_number} - {int((lines_processed / total_lines) * 100)}%'
    draw.text((0, image_size[1] - height), footer_text, font=font, fill='black')
    images.append(current_image)

    for i, img in enumerate(images):
        output_path = os.path.join(output_folder, f'page_{i+1}.bmp')
        img.save(output_path)
        print(f'Saved: {output_path}')  # Debugging line
text_to_image('input.txt', 'output_folder', 'simsun.ttc', paragraph_spacing=0)
