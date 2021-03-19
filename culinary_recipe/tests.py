perem = 'step_set-4-image'
arr = ['a', 'b', 'w']
if 'step' in perem:
    new_arr = perem.split('-')
    try:
        print(arr[int(new_arr[1])])
    except:
        print('eto bolshe')
        pass

