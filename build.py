import os

cmd='pyinstaller --clean --onefile --windowed --add-data "./fig/*.png;fig/" --name bancada main.py'
#cmd='pyinstaller --clean --onefile --windowed --icon="./fig/icon.ico" --add-data "./fig/*.png;fig/" --name bancada main.py'


os.system(cmd)