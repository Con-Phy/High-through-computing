#/usr/bin/python
def parseXyz(fname,out_dir,cores):
  import re
  import os
  temp = fname.split('.')
  pbs_name = temp[0]
  input_file = temp[0]+'_s0.com'
  input_pbs = temp[0]+'_s0.pbs'
  out_chk = temp[0]+'_s0.chk'
  out_log = temp[0]+'_s0.log'
  temp = temp[0].split('_')
  molecular = temp[1]

  in_object = open(fname,'r')
  res_list = []
  while 1:
    line = in_object.readline()
    if not line:
      break
    res = re.match(r'[^0-9]((\s*)(-*)([0-9]+(\.+)[0-9]*)(.*)){4}',line)
    if res:
      res_list.append(line)
  print res_list
  in_object.close()
  
  os.chdir(out_dir)
  out_object = open(input_file,'w')
  out_object.write('%chk='+out_chk)
  out_object.write('\n')
  out_object.write('%mem=4GB') 
  out_object.write('\n')
  out_object.write('%nprocshared='+cores)
  out_object.write('\n')
  out_object.write('#p opt B3LYP/6-31G* freq')
  out_object.write('\n')
  out_object.write('\n')
  out_object.write(molecular+' optimization with B3LYP')
  out_object.write('\n')
  out_object.write('\n')
  out_object.write('0 1')
  out_object.write('\n')
  for line in res_list:
    temp = line.split('\t')
    out_object.write(temp[0])
    out_object.write('  ')
    if float(temp[1]) < 0:
      out_object.write('%.10f' % float(temp[1]))
    else:
      out_object.write(' ')
      out_object.write('%.10f' % float(temp[1]))
    out_object.write('  ')
    if float(temp[2]) < 0:
      out_object.write('%.10f' % float(temp[2]))
    else:
      out_object.write(' ')
      out_object.write('%.10f' % float(temp[2]))
    out_object.write('  ')
    if float(temp[3]) < 0:
      out_object.write('%.10f' % float(temp[3]))
    else:
      out_object.write(' ')
      out_object.write('%.10f' % float(temp[3]))
    out_object.write('\n')
  out_object.write('\n')
  out_object.close()
  out_object = open(input_pbs,'w')
  out_object.write('#PBS -S /bin/bash\n')
  out_object.write('#PBS -N'+'  '+pbs_name+'\n')
  out_object.write('#PBS -l nodes=1:ppn=4\n')
  out_object.write('#PBS -l walltime=100000:00:00\n')
  out_object.write('cd $PBS_O_WORKDIR\n')
  out_object.write('g09 < '+input_file+'>'+out_log+'\n')
  out_object.close()
  os.system('qsub '+input_pbs)

def genInput(states,files,cores):
  import os
  out_dir = os.path.abspath(states)
  os.chdir(out_dir)
  parseXyz(files,out_dir,cores)
