#usr/bin/python
root_dir = '/home/qhuang/HzwDb/gdb'
cores = '4'
import os
import genfiles
import geninputs0
import geninputs1
import geninputt1
for files in os.listdir(root_dir):
  if os.path.isfile(os.path.join(root_dir,files)):
    #print files
    temp = files.split('.')
    molecular_dir = root_dir + '/' + temp[0]
    genfiles.genFiles(root_dir,files)
    geninputs0.genInput(molecular_dir,files,cores)
    geninputs1.genInput(molecular_dir,files,cores)
    geninputt1.genInput(molecular_dir,files,cores)

