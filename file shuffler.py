import random
import glob
import shutil

path = 'E:\Cywilizacja 69\Zgadywanki\Rozdzielczość/runda2'
sub = glob.glob(path + '/*')
files = []
for subfolder in sub:
    files.extend(glob.glob(subfolder + '/*'))
print(files)
random.shuffle(files)
for i, file in enumerate(files):
    shutil.copy(file, path + f'/{i + 1:02d}.jpg')
