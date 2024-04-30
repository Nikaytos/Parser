import os
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
font_path = 'arial.ttf'
site = 'https://www.asorti.store/'

first_category = {
    "Постільна білизна",
    "Бязь Голд",
    "Дитяча постільна білизна",
    "Страйп Сатин",
    "Батерфляй",
    "Байка",
    "Зимова тепла (плюш, велюр) постільна білизна",
    "Літні ковдри ОДА",
    "Ковдри ОДА мікрофібра холофайбер 500грм/м2",
    "Ковдри Соти Екопух",
    "Ковдри Принт холофайбер 500грм/м2",
    "Ковдра довгий ворс Травка холофайбер",
    "Покривала",
    "Вафельне покривало",
    "Велюрові покривала",
    "Плед - покривало Норка",
    "Плед-Покривало Шарпей Клітинки",
    "Покривала Кролик",
    "Стібана Клітинка",
    "Шарпей",
    "Шарпей Полуторка"
}


def create_album(url, category_name, selected_checkboxes):

    if not os.path.exists('screens'):
        os.makedirs('screens')

    safe_category_name = category_name.replace('/', '_')
    if not os.path.exists(f'screens/{safe_category_name}'):
        os.makedirs(f'screens/{safe_category_name}')

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find_all(class_='product-layout')

    if category_name in first_category:
        categories = {
            "Півтораспальний": [product for product in products if
                                product.find(lambda tag: tag.name == 'span' and 'Півтораспальний' in tag.text)],
            "Двохспальний": [product for product in products if
                             product.find(lambda tag: tag.name == 'span' and 'Двохспальний' in tag.text)],
            "Євро": [product for product in products if
                     product.find(lambda tag: tag.name == 'span' and 'Євро' in tag.text)],
            "Сімейний": [product for product in products if
                         product.find(lambda tag: tag.name == 'span' and 'Сімейний' in tag.text)],
            "Прост. 220х250": [product for product in products if
                               product.find(lambda tag: tag.name == 'span' and 'Прост. 220х250' in tag.text)]
        }

        for selected_category in selected_checkboxes:
            category_products = categories[selected_category]
            if len(category_products) > 0:
                create_albums_by_size(category_products, selected_category, category_name)

    elif category_name == "В ліжечко":
        create_albums_by_size(products, "В ліжечко", category_name)

    elif category_name == "Подушки":
        categories = {
            "50/70": [product for product in products if
                      product.find(lambda tag: tag.name == 'span' and '50/70' in tag.text)],
            "70/70": [product for product in products if
                      product.find(lambda tag: tag.name == 'span' and '70/70' in tag.text)],
        }

        for selected_category in selected_checkboxes:
            category_products = categories[selected_category]
            if len(category_products) > 0:
                create_albums_by_size(category_products, selected_category, category_name)

    elif category_name == "Дитячі пледики":
        create_albums_by_size(products, "100см*110см", category_name)


def create_albums_by_size(size, size_name, category_name):
    safe_category_name = category_name.replace('/', '_')
    safe_size_name = size_name.replace('/', '_')

    if not os.path.exists(f'screens/{safe_category_name}/{safe_size_name}'):
        os.makedirs(f'screens/{safe_category_name}/{safe_size_name}')

    chunks = [size[i:i + 25] for i in range(0, len(size), 25)]

    columns = 5
    rows = 5
    image_padding = 10
    row_padding = 20

    photo_width = 150
    photo_height = 150
    max_text_height = 0

    for index, chunk in enumerate(chunks):

        if len(size) <= 1:
            columns = 1
            rows = 1
        elif len(size) <= 2:
            columns = 2
            rows = 1
        elif len(size) <= 4:
            columns = 2
            rows = 2
        elif len(size) <= 9:
            columns = 3
            rows = 3
        elif len(size) <= 16:
            columns = 4
            rows = 4

        for product in chunk:
            product_name = product.find('h6').text.strip()
            font_size = 12
            font = ImageFont.truetype(font_path, font_size)
            draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
            text_width, text_height = draw.textsize(product_name, font=font)
            max_text_height = max(max_text_height, text_height)

        album_height = rows * (photo_height + row_padding) + row_padding + max_text_height

        album_width = columns * (photo_width + image_padding) + image_padding
        album = Image.new('RGB', (album_width, album_height), color='white')

        draw = ImageDraw.Draw(album)
        font_size = 16
        font = ImageFont.truetype(font_path, font_size)
        text = f'{category_name} - {size_name}'
        text_width, text_height = draw.textsize(text, font=font)
        draw.text(((album_width - text_width) // 2, row_padding // 2), text, fill='black', font=font)

        x_offset = image_padding
        y_offset = row_padding + text_height
        for product in chunk:
            product_name = product.find('h6').text.strip()

            img_url = product.find('img')['src']
            full_url = site + img_url
            img_response = requests.get(full_url, headers=headers)
            img = Image.open(BytesIO(img_response.content))

            img = img.resize((photo_width, photo_height), Image.ANTIALIAS)

            new_img = Image.new('RGB', (photo_width, photo_height + 30), color='white')
            new_img.paste(img, (0, 0))

            draw = ImageDraw.Draw(new_img)
            font_size = 12
            font = ImageFont.truetype(font_path, font_size)
            text_width, text_height = draw.textsize(product_name, font=font)
            while text_width > photo_width:
                font_size -= 1
                font = ImageFont.truetype(font_path, font_size)
                text_width = draw.textlength(product_name, font=font)

            draw.text(((photo_width - text_width) // 2, photo_height), product_name, fill='black', font=font)

            album.paste(new_img, (x_offset, y_offset))

            x_offset += photo_width + image_padding
            if x_offset >= album_width:
                x_offset = image_padding
                y_offset += photo_height + row_padding

        album.save(f'screens/{safe_category_name}/{safe_size_name}/{safe_category_name}_{safe_size_name}_Альбом_{index + 1}.png')

        print(f"Альбом '{safe_category_name}_{safe_size_name}_Альбом_{index + 1}.png' збережено.")
