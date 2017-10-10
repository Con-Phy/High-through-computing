#/usr/bin/python
def genFiles(molecular_dir):
  import os
  import shutil
  
  os.chdir(molecular_dir)
  os.mkdir('s0')
  os.mkdir('s1')
  os.mkdir('t1')
  os.mkdir('nacme')
  os.mkdir('numfraq')
