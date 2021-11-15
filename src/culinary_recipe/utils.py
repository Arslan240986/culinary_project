import uu
import os
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.conf import settings

def make_slug(value):
    dictiner = {'д':'d', 'а': 'a', 'г': 'g', 'р': 'r', 'с': 's', 'л': 'l', 'ж': 'zh', 'н': 'n', 'б': 'b', 'и': 'i', 'э': 'e', 'х': 'h',
                'з':'z', 'т': 't', 'м': 'm', 'у': 'u', 'ф': 'f', 'й': 'y', 'я': 'ya', 'к': 'k', 'п': 'p', 'о': 'o',
                'е':'ye', 'ё':'yo', 'ч':'ch', 'ш':'sh', 'ы':'y', 'в':'v',  'ц':'s', 'в':'w'}
    arr = list(value.lower())
    num = 0
    for i in arr:
        if i in dictiner.keys():
            arr[num] = dictiner[i]
        elif i in dictiner.values():
            arr[num] = i
        else:
            arr[num] = '-'
        num += 1
    result = ''.join(arr)
    return result



def getMonth(num):
    month_array = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
                   'ноябрь', 'декабрь']
    arr = [n for n in num ]

    if arr[0] == 0:
        return month_array[int(arr[1])-1]
    else:
        return month_array[int(num)-1]


def watermark_photo(input_image_path,
                    output_image_path,
                    watermark_image_path,
                    name_path,
                    position):
    new_name = output_image_path.split('.')
    base_image = Image.open(input_image_path)
    im_io = BytesIO()
    watermark = Image.open(watermark_image_path)
    width, height = base_image.size
    if width > 1200:
        base_image.thumbnail((1200, 1200))
        width, height = base_image.size
    transparent = Image.new('RGB', (width, height), (0,0,0,0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    try:
        os.makedirs(f'{settings.MEDIA_ROOT}/{name_path}')
    except FileExistsError:
        # directory already exists
        pass
    transparent.save(f'{settings.MEDIA_ROOT}/{name_path}/{new_name[0]}.webp', 'WEBP',)
    transparent.close()
    new_one = Image.open(f'{settings.MEDIA_ROOT}/{name_path}/{new_name[0]}.webp')
    new_one.save(im_io, 'WEBP')
    new_image = File(im_io, name=f'{new_name[0]}.webp')
    return new_image