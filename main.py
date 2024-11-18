import ctypes
import os
import random
import keyboard
import time
import threading

from pystray import Icon, MenuItem, Menu
from config import WallpaperFolderPath
from PIL import Image

wallpapersFolder = WallpaperFolderPath

wallpapers = []
wallpaperChanged = False

def updateWallpapers():
	global wallpapers
	wallpapers = [i for i in os.listdir(wallpapersFolder) if i.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))]


def wallpaperChanger():
	if wallpapers:
		randomWallpaper = random.choice(wallpapers)
		wallpaperPath = os.path.join(wallpapersFolder, randomWallpaper)

		SPI_SETDESKWALLPAPER = 20
		ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaperPath, 3)
		wallpaperChanged = True
	else:
		print('[*] There is no wallpaper in folder!')

def createTrayIcon():
	image = Image.open(r'assets\icon.jpg')

	menu = Menu(
		MenuItem('Change Wallpaper', lambda: wallpaperChanger()),
		MenuItem('Exit', lambda icon, item: icon.stop())
	)

	icon = Icon('wallpaper_changer', image, 'Wallpaper Changer', menu)
	icon.run()

def onHotKeyPressed():
	global wallpaperChanged
	if not wallpaperChanged:
		wallpaperChanger()

def backgroundWallpaperUpdater():
	while True:
		updateWallpapers()

		if keyboard.is_pressed('win+alt') and not wallpaperChanged:
			wallpaperChanger()

		if not keyboard.is_pressed('win+alt'):
			wallpaperChanged = False

		time.sleep(0.1)

if __name__ == '__main__':
	threading.Thread(target=backgroundWallpaperUpdater, daemon=True).start()
	createTrayIcon()