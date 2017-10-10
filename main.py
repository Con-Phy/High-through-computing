#usr/bin/python
root_dir = '/home/qhuang/HzwDb/gdb'
cores = '4'
import os
import shutil
import genfiles
import geninput

for files in os.listdir(root_dir):
  if os.path.isfile(os.path.join(root_dir,files)):
    temp = files.split('.')
    molecular_dir = os.path.join(root_dir,temp[0])

    os.chdir(root_dir)
    os.mkdir(molecular_dir)
    shutil.move(files,molecular_dir)
    genfiles.genFiles(molecular_dir)

    os.chdir(molecular_dir)
    geninput.genInput(files,molecular_dir,'s0',cores)
    os.chdir(molecular_dir)
    geninput.genInput(files,molecular_dir,'s1',cores)
    os.chdir(molecular_dir)
    geninput.genInput(files,molecular_dir,'t1',cores)

