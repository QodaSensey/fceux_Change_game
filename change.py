#from pywinauto.application import Application
import pywinauto
#import keyboard
import time
import random
import shutil
from ctypes import *
import sys

# здесь определяется разрядность архитектуры
is_64bit_arch = sys.maxsize > 2**32
# необходимые типы 
LONG_PTR = c_longlong if is_64bit_arch else c_long
UINT_PTR = c_ulonglong if is_64bit_arch else c_uint
UINT = c_uint
HANDLE = c_void_p
WPARAM = UINT_PTR
LPARAM = LONG_PTR
LRESULT = LONG_PTR
HWND = HANDLE
LPCSTR = c_char_p
DWORD = c_ulong
WORD = c_ushort
SendMessage = windll.user32.SendMessageA
FindWindow = windll.user32.FindWindowA
MapVirtualKey = windll.user32.MapVirtualKeyA

# фнукция нажатия и отпускания клавиши
def press_key(key_vk, window_title):
    c_window_title = LPCSTR(window_title.encode('utf-8'))
    WM_KEYUP = UINT(0x0101)
    WM_KEYDOWN = UINT(0x0100)
    wParam = WPARAM(key_vk)
    key_sc = MapVirtualKey(key_vk, 0)
    lParam = LPARAM(0x1 | (key_sc << 16))
    lParamDown = LPARAM(1 + (key_sc << 16) + (1 << 30))
    lParamUp = LPARAM(1 + (3 << 30) + (key_sc << 16))
    # находим хендл окна
    handle = FindWindow(LPCSTR(), c_window_title)
    print(handle)    
    # отправляем сообщение о нажатии клавиши
    SendMessage(handle, WM_KEYDOWN, wParam, lParamDown) 
    # отправляем сообщение об отпускании клавиши
    return SendMessage(handle, WM_KEYUP, wParam, lParamUp) 

PATH_ROMS = 'fcs\\'
START_ROM = '1.fc0'
TAIMER = 10
EMUL_NAME = 'FCEUX 2.4.0-interim gitcd4d22cc6a3d92c6a1a93832975b68d5473feec5: 1'
roms = ['Super Mario Brothers 2 (Japan).fc0','Galaxian (1990)(Namco Ltd.).fc0','Super Lode Runner (Japan) [b].fc0']
#kol_roms = len(roms)
cur_rom = 'Super Mario Brothers 2 (Japan).fc0'

# Копируем файлы roms в номер.fc0
#for i in range(kol_roms):
#    shutil.copyfile(PATH_ROMS+roms[i], PATH_ROMS+str(i)+'.fc0')
#app = pywinauto.Application().start('fceux64.exe')
app = pywinauto.Application().connect(path='fceux64.exe')
emul = app['FCEUX 2.4.0-interim gitcd4d22cc6a3d92c6a1a93832975b68d5473feec5: 1']
timing = time.time()
while True:
    if time.time() - timing > TAIMER:
            # сохраняем состояние
#        keyboard.send('I')
#        press_key(0x49, EMUL_NAME)
#        app.fceux64.TypeKeys('I')
        print("File->Savestate->Save State")
        emul.menu_select("File->Savestate->Save State")
            # копируем файл состояния в нужный ром
        shutil.copyfile(PATH_ROMS+START_ROM, PATH_ROMS+cur_rom)
            # выбираем случайный ром
        cur_rom = random.choice(roms)
        print(cur_rom)
            # копируем файл из выбранного рома в START_ROM
        shutil.copyfile(PATH_ROMS+cur_rom, PATH_ROMS+START_ROM)
            # загружаем состояние
#        keyboard.send('P')
#        press_key(0x50, EMUL_NAME)
#        app.fceux64.TypeKeys('P')
        emul.menu_select("File->Savestate->Load State")
        print("File->Savestate->Load State")
            # перезапускаем таймер
        timing = time.time()

