#!/usr/bin/python
root_dir = '/home/qhuang/HzwDb/gdb'
cores = '1'
import os
import shutil
import genfiles
import geninput
from time import sleep

for files in os.listdir(root_dir):
  if os.path.isfile(os.path.join(root_dir,files)):
    temp = files.split('.')
    molecular_dir = os.path.join(root_dir,temp[0])

    os.chdir(root_dir)
    os.mkdir(molecular_dir)
    shutil.move(files,molecular_dir)
    genfiles.genFiles(molecular_dir)
    numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))

    while 1:
      if numofjob<52:
      	a = os.popen('qstat | grep qhuang | wc -l')
      	b = int(a.read())
      	if b<52:
          if os.path.exists(molecular_dir):
            os.chdir(molecular_dir)
            geninput.genInput(files,molecular_dir,'s0',cores)
          break
      sleep(180)
      numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
    sleep(2)
    numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
    while 1:
      if numofjob<52:
      	a = os.popen('qstat | grep qhuang | wc -l')
      	b = int(a.read())
      	if b<52:
          if os.path.exists(molecular_dir):
            os.chdir(molecular_dir)
            geninput.genInput(files,molecular_dir,'s1',cores)
          break
      sleep(180)
      numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
    sleep(2)
    numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
    while 1:
      if numofjob<52:
      	a = os.popen('qstat | grep qhuang | wc -l')
      	b = int(a.read())
      	if b<52:
          if os.path.exists(molecular_dir):
            os.chdir(molecular_dir)
            geninput.genInput(files,molecular_dir,'t1',cores)
          break
      sleep(180)
      numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
    sleep(2)


