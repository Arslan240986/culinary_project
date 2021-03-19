import uu

def make_slug(value):
    dictiner = {'д':'d', 'а': 'a', 'р': 'r', 'с': 's', 'л': 'l', 'ж': 'zh', 'н': 'n', 'б': 'b', 'и': 'i', 'э': 'e', 'х': 'h',
                'з':'z', 'т': 't', 'м': 'm', 'у': 'u', 'ф': 'f', 'й': 'y', 'я': 'ya', 'к': 'k', 'п': 'p', 'о': 'o',
                'е':'ye', 'ё':'yo', 'ч':'ch', 'ш':'sh', 'ы':'y', 'в':'v',  'ц':'s'}
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