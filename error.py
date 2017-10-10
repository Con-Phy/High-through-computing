#usr/bin/python
import os
import re
import math
root_dir = '/home/qhuang/HzwDb/gdb'
desti_dir = '/home/qhuang/HzwDb/gdb_error/'
n=0
for dirs in os.listdir(root_dir):
  dirs = root_dir+'/'+dirs
  for files in os.walk(dirs):
    for name in files[2]:
      if re.match(r'.*\.log',name,flags=0):
        os.chdir(files[0])
        process = os.popen("grep 'Error termination' "+name)
        errorinfo = process.read()
        process.close()
        if errorinfo:
          n = n+1
          if os.path.exists(dirs):
            os.system('mv '+dirs +' '+desti_dir)
            #with open('/home/qhuang/HzwDb/error.txt','a') as file:
              #file.write(dirs)
              #file.write('\n')
            #file.write(errorinfo)
            #file.write('\n')
print(n)
      
