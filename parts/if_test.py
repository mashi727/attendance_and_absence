# coding: utf-8


COLOR='RED'

import platform
osname = platform.system()
if osname == 'Darwin':
    if COLOR == 'RED':
        print('RED ON')
    elif COLOR == 'BLUE':
        print('BLUE ON')
    elif COLOR == 'YELLOW':
        print('YELLOW ON')

elif osname == 'Linux':
    if COLOR == 'RED':
        GPIO_NUM = 16
    elif COLOR == 'BLUE':
        GPIO_NUM = 20
    elif COLOR == 'YELLOW':
        GPIO_NUM = 21

# for文で、breakしない
print('im here')
