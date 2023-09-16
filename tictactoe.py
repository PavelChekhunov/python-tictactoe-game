"""
Игра крестики-нолики.
Инра игрока с компьютером
Для совершения хода необходимо указать новер строки и номер столбца через запятую или пробел,
или номер ячейки игрового поля.
Номера строк и столбцов обозначены в заголовках инрового поля.
Пример ввода: 1, 2 или 7 или 2  0
Выход в любой момент: q
"""

import random, time, os

os.system("")

num_cells = 3
win_board = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
players = ('X', '0')
area_steps = ['']*num_cells**2
CRED = '\033[91m'
CEND = '\033[0m'
CGYAN = '\033[96m'
CYELLOW = '\033[93m'
CBACKWIN = '\x1b[0;30;43m' #'\033[43m'


def get_cell_data(idx, wincells=None):
    t = ' ' * 3
    if area_steps[idx].strip():
        t = f' {area_steps[idx]} '
        if wincells and idx in wincells:
            t = f'{CBACKWIN}{t}{CEND}'
    return t


def draw_to_console(wincells=None):
    print(' ' * 5, end='')
    for i in range(num_cells):
        print(f'   {i}  ', end='')
    print()
    print(' ' * 4,'_', end='')
    print('_' * 6 * num_cells)
    for i in range(num_cells):
        print(' ' * 2, i,  '|', get_cell_data(i * 3, wincells), '|',
              get_cell_data(i * 3 + 1, wincells), '|', get_cell_data(i * 3 + 2, wincells), '|')
    print(' ' * 4, '-', end='')
    print('-' * 6 * num_cells)


def validate_enter(txt):
    n = -1
    try:
        lt = list(map(int, txt.replace(',', ' ').split()))
    except (ValueError, Exception):
        return n

    if len(lt) == 0:
        return n
    elif len(lt) > 1:
        n = lt[0] * num_cells + lt[1]
    else:
        n = lt[0]
    return n


def check_usage(ncell):
    if 0 <= ncell < len(area_steps):
        return area_steps[ncell] == ''
    else:
        return False


def check_winner(sign):
    for t in win_board:
        n = len([i for i in t if area_steps[i] == sign])
        if n > 2:
            return t
    return None


def list_sign(sign):
    return [i for i, v in enumerate(area_steps) if v == sign]


def ai_light_decor(func):
    def wrapper():
        for t in win_board:
            e, c = 0, 0
            for x in t:
                if area_steps[x] == players[1]:
                    c += 1
                elif area_steps[x] == '':
                    e += 1
            if c == 2 and e == 1:
                return [x for x in t if area_steps[x] == ''][0]
        for t in win_board:
            e, p = 0, 0
            for x in t:
                if area_steps[x] == players[0]:
                    p += 1
                elif area_steps[x] == '':
                    e += 1
            if p == 2 and e == 1:
                return [x for x in t if area_steps[x] == ''][0]
        return func()
    return wrapper


@ai_light_decor
def comp_step():
    return random.choice(list_sign(''))


def game_run():
    print('Игра крестики-нолики.')
    result = None
    while True:
        draw_to_console()
        txt = input('\nВведите номера строки и столбца через пробел или запятую, или номер ячейки:')
        if txt[0].lower() == 'q':
            break
        ncell = validate_enter(txt)
        if 0 > ncell or ncell >= num_cells ** 2:
            print(f'{CRED}Введены неверные данные!{CEND}')
            continue
        if not check_usage(ncell):
            print(f'{CRED}Ячейка уже имеет значение!{CEND}')
            continue
        print(f'enter {ncell}')
        area_steps[ncell] = players[0]
        result = check_winner(players[0])
        if result is not None:
            print(CGYAN,'*' * 9, 'ВЫ ВЫИГРАЛИ!!!', '*' * 9, CEND)
            break
        if len(list_sign('')) < 1:
            print('-' * 9, 'Ничья!', '-' * 9)
            break
        time.sleep(0.3)
        ncell = comp_step()
        if 0 <= ncell <= num_cells ** 2:
            area_steps[ncell] = players[1]
            print(f'Компьютер сделал свой ход! {ncell}')
        else:
            print(f'{CRED}Компьютер не смог сделать свой ход!{CEND}')
            break
        result = check_winner(players[1])
        if result is not None:
            print(CRED,'*' * 9, 'ВЫ проиграли!', '*' * 9, CEND)
            break
        if len(list_sign('')) < 1:
            print('-' * 9, 'Ничья!', '-' * 9)
            break
    draw_to_console(result)
    print('Игра завершена.')


game_run()
