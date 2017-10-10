#/usr/bin/python
def genFiles(root_dir,files):
  import os
  import shutil
  os.chdir(root_dir)
  temp = files.split('.')
  molecular_dir = root_dir + '/' + temp[0]
  os.mkdir(molecular_dir)
  shutil.move(files,molecular_dir)
  os.chdir(molecular_dir)
  os.mkdir('s0')
  os.mkdir('s1')
  os.mkdir('t1')
  os.mkdir('nacme')
  os.mkdir('numfraq')
