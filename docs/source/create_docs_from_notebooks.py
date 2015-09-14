# -*- coding: utf-8 -*-
"""
Utility to create the docs from notebooks
"""
import os
import shutil
from glob import glob
import time
import fnmatch
import fileinput

# Convert notebooks to rst docs
os.chdir('notebooks')

files = glob('*.ipynb')
files.sort()
print("The following files will be converted to rst")
print(files)

for nb in files:
    title = nb[4:-6]
    conversion = 'jupyter nbconvert "{0}" --to rst --output "{1}.rst"'
    print(conversion.format(nb, title))
    os.system(conversion.format(nb, title))

# We stop the program to allow nbconvert to finish
time.sleep(10)

# Move the rst files to the source folder and
# modify the path to images in the rst files
dst = os.path.join(os.getcwd(), '..')
files = glob("*.rst")
print("Copying converted notebook files to ", dst)
print(files)
for rst in files:
    orig = rst.split('.')[0] + '_files%5C'
    new = '_static/'
    for line in fileinput.input(rst, inplace=True):
        print(line.replace(orig, new), end='')
    shutil.copy(rst, os.path.join(dst, "{}".format(rst.replace('_', ' '))))
    os.remove(rst)

# Move the png inages to the source/_static/ folder
dst = os.path.join(os.getcwd(), '..' + os.sep + '_static')
matches = []
for root, dirnames, filenames in os.walk('.'):
  for filename in fnmatch.filter(filenames, '*.png'):
    matches.append(os.path.join(root, filename))
print("Copying files to ", dst)
print(matches)
for png in matches:
    shutil.copy(png, os.path.join(dst, "{}".format(png.split(os.sep)[-1])))

# Make the docs
os.chdir('..')
os.chdir('..')
os.system('make html')

print('Finish')