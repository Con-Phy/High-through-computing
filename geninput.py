#/usr/bin/python
import os
import re
def genInput(files,dirs,states,cores):
  out_dir = os.path.join(dirs,states)
  #parseXyz(files,out_dir,states,cores)
#def parseXyz(files,out_dir,states,cores): 
  g09_parameters = []
  memories = '4'
  temp = files.split('.')
  pbs_name = temp[0]
  input_file = temp[0]+'_'+states+'.com'
  input_pbs = temp[0]+'_'+states+'.pbs'
  out_chk = temp[0]+'_'+states+'.chk'
  out_log = temp[0]+'_'+states+'.log'
  temp = temp[0].split('_')
  molecular = temp[1]
  pp = 'B3LYP'
  if states == 's0':
    compute_para2 = '0 1'
    compute_para1 = '#p opt B3LYP/6-31G* freq'
  if states == 's1':
    compute_para2 = '0 1'
    compute_para1 = '#p opt td B3LYP/6-31G* freq'
  if states == 't1':
    compute_para2 = '0 3'
    compute_para1 = '#p opt B3LYP/6-31G* freq'
  g09_parameters.append(out_chk)
  g09_parameters.append(memories)
  g09_parameters.append(cores)
  g09_parameters.append(compute_para1)
  g09_parameters.append(molecular)
  g09_parameters.append(pp)
  g09_parameters.append(compute_para2)
  g09_parameters.append(input_file)
  g09_parameters.append(out_log)
  g09_parameters.append(pbs_name)
  g09_parameters.append(input_pbs)


  with open(files,'r') as in_object:
    coodinates = []
    while 1:
      line = in_object.readline()
      if not line:
        break
      res = re.match(r'[^0-9]((\s*)(-*)([0-9]+(\.+)[0-9]*)(.*)){4}',line)
      if res:
        coodinates.append(line)

  #writeInput(g09_parameters,coodinates,out_dir)

#def writeInput(g09_parameters,coodinates,out_dir):
  os.chdir(out_dir)
  with open(g09_parameters[7],'w') as out_object:
    out_object.write('%chk='+g09_parameters[0])
    out_object.write('\n')
    out_object.write('%mem='+g09_parameters[1]+'GB') 
    out_object.write('\n')
    out_object.write('%nprocshared='+g09_parameters[2])
    out_object.write('\n')
    out_object.write(g09_parameters[3])
    out_object.write('\n')
    out_object.write('\n')
    out_object.write(g09_parameters[4]+' optimization with '+g09_parameters[5])
    out_object.write('\n')
    out_object.write('\n')
    out_object.write(g09_parameters[6])
    out_object.write('\n')
    for line in coodinates:
      res = re.match(r'[^0-9]((\s*)(-*)([0-9]+(\.+)[0-9]*)(\s*)){4}',line)
      if res:
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
      else:
        print line
        desti_dir = '/home/qhuang/HzwDb/gdb_error/'
        os.system('mv '+dirs +' '+desti_dir)
        return
    out_object.write('\n')
  with open(g09_parameters[10],'w') as out_object:
    out_object.write('#PBS -S /bin/bash\n')
    out_object.write('#PBS -N'+'  '+g09_parameters[9]+'\n')
    out_object.write('#PBS -l nodes=1:ppn='+g09_parameters[2]+'\n')
    out_object.write('#PBS -l walltime=100000:00:00\n')
    out_object.write('cd $PBS_O_WORKDIR\n')
    out_object.write('echo "gaussian" >>/home/qhuang/HzwDb/jobnumber/job.log\n')
    out_object.write('g09 < '+g09_parameters[7]+'>'+g09_parameters[8]+'\n')
    out_object.write("sed -i '$d' /home/qhuang/HzwDb/jobnumber/job.log\n")
  os.system('qsub '+g09_parameters[10])


