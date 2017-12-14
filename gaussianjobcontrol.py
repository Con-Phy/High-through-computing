import os
import re
import shutil
from time import sleep
class GaussianJobControl():
  def __init__(self,cores,root_dir):
    self.cores = cores
    self.root_dir = root_dir

  def generate_files(molecular_dir):
    dirs = molecular_dir+'/s0'
    os.chdir(molecular_dir)
    if os.path.exists(dirs):
      os.mkdir('s0')
    dirs = molecular_dir+'/s1'
    if os.path.exists(dirs):
      os.mkdir('s1')
    dirs = molecular_dir+'/t1'
    if os.path.exists(dirs):
      os.mkdir('t1')
    dirs = molecular_dir+'/nacme'
    if os.path.exists(dirs):
      os.mkdir('nacme')
    dirs = molecular_dir+'/numfraq'
    if os.path.exists(dirs):
      os.mkdir('numfraq')
    dirs = molecular_dir+'/optic'
    if os.path.exists(dirs):
      os.mkdir('optic')
  
  def generate_input(files,dirs,states,cores):
    out_dir = os.path.join(dirs,states)
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

  def submission_control(self):
    for files in os.listdir(self.root_dir):
      if os.path.isfile(os.path.join(self.root_dir,files)):
        temp = files.split('.')
        molecular_dir = os.path.join(root_dir,temp[0])
      
        os.chdir(root_dir)
        os.mkdir(molecular_dir)
        shutil.move(files,molecular_dir)
        generate_files(molecular_dir)
        numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
      
        while 1:
          if numofjob<52:
          	a = os.popen('qstat | grep qhuang | wc -l')
          	b = int(a.read())
          	if b<52:
              if os.path.exists(molecular_dir):
                os.chdir(molecular_dir)
                generate_input(files,molecular_dir,'s0',self.cores)
              break
          sleep(180)
          numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
        sleep(5)
        numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
        while 1:
          if numofjob<52:
          	a = os.popen('qstat | grep qhuang | wc -l')
          	b = int(a.read())
          	if b<52:
              if os.path.exists(molecular_dir):
                os.chdir(molecular_dir)
                generate_input(files,molecular_dir,'s1',self.cores)
              break
          sleep(180)
          numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
        sleep(5)
        numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
        while 1:
          if numofjob<52:
          	a = os.popen('qstat | grep qhuang | wc -l')
          	b = int(a.read())
          	if b<52:
              if os.path.exists(molecular_dir):
                os.chdir(molecular_dir)
                generate_input(files,molecular_dir,'t1',self.cores)
              break
          sleep(180)
          numofjob = sum(1 for line in open('/home/qhuang/HzwDb/jobnumber/job.log'))
        sleep(5)

  def str_to_13(via):
  	num = 13 - len(vib)
    temp = ' '*num
    return temp+vib

  def parse_log_s0(fname):
      #
    #begin to parse *.com file to obtain atom symbol, atom number and charge of molecular
    atom_syb = []
    temp = fname.split('.')
    fname1 = temp[0]+'.com'
    #print fname1
    with open(fname1,'r') as in_object:
      while 1:
        line = in_object.readline()
        if not line:
          break
        #find charge value in .com file
        res = re.match(r'[0-9]\s*[0-9]',line)  
        if res:
          temp = line.split(' ')
          atom_syb.append(temp[0])
        #find atom symbol in .com file
        res = re.match(r'[^0-9]((\s*)(-*)([0-9]+(\.+)[0-9]*)(.*)){3}',line)
        if res:
          temp = line.split(' ')
          atom_syb.append(temp[0])
    charge = atom_syb[0]
    atom_num = len(atom_syb)-1
    #end to parse *.com file
    #
  
    #
    base_name = os.path.basename(fname)
    temp = base_name.split('_')
    molecular = temp[1] #molecular symbol
    number = temp[0]    #file number in gdb
    temp = []
    mulliken = []
    atom_pos = []
    atom_mass = []
    frequency = ''
    frequencies = []
    vibration = []
    #varible to store 17 basic properties
    res_list = []       
    #medium varibles
    res_list1 = []
    res_list2 = []
    res_list3 = []
    res_list4 = []
    res_list5 = []
    res_list6 = []
    res_list7 = []
    res_list8 = []
    res_list9 = []
    res_list10 = []
    res_list11 = []
    res_list12 = []
    res_list13 = []
    res_list14 = []
    i = 0
    #begin to parse *.log file 
    #
    #
    with open(fname,'r') as in_object:
      while 1:
        line = in_object.readline()
        if not line:
          break
        res = re.match(r' Rotational constants',line)
        if res:
          res_list1.append(line)
        res = re.match(r' Dipole moment',line)
        if res:
          line = in_object.readline()
          #print line
          res_list2.append(line)
        res = re.match(r' Isotropic polarizability',line)
        if res:
          res_list3.append(line)
        res = re.match(r' Alpha',line)
        if res:
          res_list4.append(line)
        res = re.match(r' Electronic spatial extent',line)
        if res:
          res_list5.append(line)
        res = re.match(r' Zero-point vibrational energy',line)
        if res:
          line = in_object.readline()
          res_list6.append(line)
        res = re.match(r' SCF Done',line)
        if res:
          res_list7.append(line)
        res = re.match(r' Sum of electronic and zero-point Energies',line)
        if res:
          line = in_object.readline()
          res_list8.append(line)
          line = in_object.readline()
          res_list9.append(line)
          line = in_object.readline()
          res_list10.append(line)
          line = in_object.readline()
          line = in_object.readline()
          line = in_object.readline()
          line = in_object.readline()
          res_list11.append(line)
        res = re.match(r'.*Standard orientation',line)
        if res:
          line = in_object.readline() 
          line = in_object.readline() 
          line = in_object.readline() 
          line = in_object.readline() 
          line = in_object.readline()
          j = 0
          while j < atom_num:
            res_list12.append(line)
            line = in_object.readline()
            j+=1
        res = re.match(r'.*Mulliken charges:',line)
        if res:
          line = in_object.readline()
          res_list13.append(line)
          j = 0
          while j < atom_num:
            res_list13.append(line)
            line = in_object.readline()
            j+=1
        res = re.match(r'.*Frequencies',line)
        if res:
          frequency = ''
          res_list15 = []
          str1 = re.compile(r'-*\d+\.\d+')
          temp = str1.findall(line)
          for i in temp:
             frequency =i+' '+frequency
          #print frequency
          frequencies.append(frequency)
          line = in_object.readline()
          line = in_object.readline()
          line = in_object.readline()
          line = in_object.readline()
          j = 0
          temp_list1 = []
          temp_list2 = []
          temp_list3 = []
          while j < atom_num:
            temp_list = []
            line = in_object.readline()
            str1 = re.compile(r'-*\d+\.\d+')
            temp = str1.findall(line)
            #print temp
            if len(temp)/3 >= 1:
              temp_list.append(temp[0])
              temp_list.append(temp[1])
              temp_list.append(temp[2])
              temp_list1.append(temp_list)
            temp_list = []
            if len(temp)/3 >=2:
              temp_list.append(temp[3])
              temp_list.append(temp[4])
              temp_list.append(temp[5])
              temp_list2.append(temp_list)
            temp_list = []
            if len(temp)/3 ==3:
              temp_list.append(temp[6])
              temp_list.append(temp[7])
              temp_list.append(temp[8])
              temp_list3.append(temp_list)
            j+=1
          if temp_list1:
            vibration.append(temp_list1)
          if temp_list2: 
            vibration.append(temp_list2)
          if temp_list3:
            vibration.append(temp_list3)
          #print vibration
        #find atom mass  
        res = re.match(r'.*Temperature',line)
        if res:
          j = 0
          while j < atom_num:
            line = in_object.readline()
            res_list14.append(line)
            j+=1
    #end parse *.log file
    #
    #begin to obtain ground state data from raw data 
    #print res_list12 
    if res_list12:          
      for i in range(atom_num):
        atom_pos.append(res_list12[-1-i])
    else:
      print molecular_dir
    str1 = re.compile(r'-*\d+\.\d+')
    if res_list1:
      temp = str1.findall(res_list1[-1])
      for i in temp:
        res_list.append(i)   #res_list[0],[1],[2] Rotational constant A B C
    if res_list2:
      temp = str1.findall(res_list2[-1])
      res_list.append(temp[-1])  #res_list[3] Dipole moment mu
    if res_list3:
      temp = str1.findall(res_list3[-1])
      res_list.append(temp[-1])  #res_list[4] Isotropic polarizability alpha
    if res_list4:
      temp = str1.findall(res_list4[-4])
      res_list.append(temp[-1])  #res_list[5] homo
    if res_list5:
      temp = str1.findall(res_list4[-3])
      res_list.append(temp[0])   #res_list[6] lomo
      lumo = float(res_list[-1])
      homo = float(res_list[-2])
      res_list.append(lumo-homo)  #res_list[7] gap
    if res_list5:
      temp = str1.findall(res_list5[-1])
      res_list.append(temp[-1])  #res_list[8] r2
    if res_list6:
      temp = str1.findall(res_list6[-1])
      temp = float(temp[-1])/627.51
      temp = str(temp)
      res_list.append(temp)   #res_list[9] zpve
    if res_list7:
      temp = str1.findall(res_list7[-1])
      res_list.append(temp[-1])   #res_list[10] SCF Done U0
    if res_list8:
      temp = str1.findall(res_list8[-1])
      res_list.append(temp[-1])   #res_list[11] 
    if res_list9:
      temp = str1.findall(res_list9[-1])
      res_list.append(temp[-1])
    if res_list10:
      temp = str1.findall(res_list10[-1])
      res_list.append(temp[-1])
    if res_list11:
      temp = str1.findall(res_list11[-1])
      res_list.append(temp[-2])
    if res_list13:
      for i in range(atom_num):
        temp = res_list13[-1-i].split(' ')
        mulliken.append(temp[-1])
    if res_list14:
      for i in res_list14:
        temp = i.split(' ')
        atom_mass.append(temp[-1])
    #end obtain ground state data from raw data
    #
    #begin to write properties to *.mols file
    # 
    with open(out_file,'w') as out_object:
      out_object.write('------------------------------Chemical Formula and Charge---------------------------------------------------------------\n')
      out_object.write(' ')
      out_object.write(molecular+"  "+charge+"\n")
      out_object.write('------------------------------SMILES------------------------------------------------------------------------------------\n')
      out_object.write(' '+smiles+'\n')
      out_object.write('------------------------------Basic properties--------------------------------------------------------------------------\n')
      out_object.write('--tag--index---A---B---C----dipole--isotropic--homo--lumo--gap--r2------zpve--U0--U--H--G--Cv---------------------------\n')
      out_object.write('--xxx--XXXXXX--GHz-GHz-Ghz--Debye---Bohr^3-----Ha----Ha----Ha---Bohr^2--Ha----Ha--Ha-Ha-Ha-cal/(mol K)------------------\n')
      out_object.write(' gdb  '+number+'  ')
      if res_list:
        for i in res_list:
          out_object.write('%.6f' % float(i))
          out_object.write('  ')
        out_object.write('\n')
      out_object.write('------------------------------Element,XYZ (Angstrom)--------------------------------------------------------------------\n')
      temp = str(atom_num)
      out_object.write(' '+temp+'\n')
      str1 = re.compile(r'-*\d+\.*\d*')
      if atom_pos:
        for i in range(atom_num):
          temp = str1.findall(atom_pos[-1-i])
          #print temp
          out_object.write(' '+atom_syb[i+1]+'  ')
          if float(temp[3])<0:
            out_object.write('%.6f' % float(temp[3]))
            out_object.write('  ')
          else:
            out_object.write(' ')
            out_object.write('%.6f' % float(temp[3]))
            out_object.write('  ')
          if float(temp[4])<0:
            out_object.write('%.6f' % float(temp[4]))
            out_object.write('  ')
          else:
            out_object.write(' ')
            out_object.write('%.6f' % float(temp[4]))
            out_object.write('  ')
          if float(temp[5])<0:
            out_object.write('%.6f' % float(temp[5]))
            out_object.write('  ')
          else:
            out_object.write(' ')
            out_object.write('%.6f' % float(temp[5]))
            out_object.write('  ')
          out_object.write('\n')
      out_object.write('------------------------------Mulliken Partial Charge (|e|)-------------------------------------------------------------\n')
      if mulliken:
        for i in mulliken:
          out_object.write(' ')
          out_object.write('%.6f' % float(i))
          out_object.write('  ')
        out_object.write('\n')
      out_object.write('------------------------------Atom Mass (Relative atomic mass)----------------------------------------------------------\n')
      if atom_mass:
        for i in atom_mass:
          out_object.write(' ')
          out_object.write('%.6f' % float(i))
          out_object.write('  ')
        out_object.write('\n')
      out_object.write('------------------------------Vibration Frequency (cm-1)----------------------------------------------------------------\n')
      if frequencies:
        for i in frequencies:
          i=i.rstrip()
          temp = i.split(' ')
          for j in temp:
            t1 = '%.6f' % float(j)
            t1=str_to_13(t1)
            out_object.write(' ')
            out_object.write(t1)
            out_object.write('  ')
          out_object.write('\n')
      out_object.write('------------------------------Vibration Modes---------------------------------------------------------------------------\n')
      if vibration:
        for i in vibration:
          for j in i:
            out_object.write(' ')
            for k in j:
              if float(k)<0:
                out_object.write('%.6f' % float(k))
                out_object.write('  ')
              else:
                out_object.write(' ')
                out_object.write('%.6f' % float(k))
                out_object.write('  ')
            out_object.write('\n')   
    #end write properties to *.mols file
  
  def parse_log_s1t1(fname,states):
  	  #
    #begin to parse *.com file to obtain atom symbol, atom number and charge of molecular
    atom_syb = []
    temp = fname.split('.')
    fname1 = temp[0]+'.com'
    with open(fname1,'r') as in_object:
      while 1:
        line = in_object.readline()
        if not line:
          break
        #find charge value in .com file
        res = re.match(r'[0-9]\s*[0-9]',line)  
        if res:
          temp = line.split(' ')
          atom_syb.append(temp[0])
        #find atom symbol in .com file
        res = re.match(r'[^0-9]((\s*)(-*)([0-9]+(\.+)[0-9]*)(.*)){3}',line)
        if res:
          temp = line.split(' ')
          atom_syb.append(temp[0])
    charge = atom_syb[0]
    atom_num = len(atom_syb)-1
    #end to parse *.com file
    #
    #energy_s1  = []
    atom_pos  = []
    res_list1 = []
    res_list2 = []
    res_list3 = []
    with open(fname,'r') as in_object:
      while 1:
        line = in_object.readline()
        if not line:
          break
        if states == 's1':
          res = re.match(r' Total Energy',line)
        if states == 't1':
          res = re.match(r' SCF Done',line)
        if res:
          res_list1.append(line)
        res = re.match(r'.*Standard orientation',line)
        if res:
          line = in_object.readline() 
          line = in_object.readline() 
          line = in_object.readline() 
          line = in_object.readline() 
          line = in_object.readline()
          j = 0
          while j < atom_num:
            res_list2.append(line)
            line = in_object.readline()
            j+=1
    str1 = re.compile(r'-*\d+\.\d+')
    if res_list1:
      temp = str1.findall(res_list1[-1])
      energy_s1 = temp[-1]
    if res_list2:
      for i in range(atom_num):
        atom_pos.append(res_list2[-1-i])
  
    with open(out_file,'a') as out_object:
      out_object.write(tokens)
      out_object.write(' '+energy_s1+note1+'\n')
      out_object.write(note2+'\n')
      str1 = re.compile(r'-*\d+\.*\d*')
      if atom_pos:
        for i in range(atom_num):
          temp = str1.findall(atom_pos[-1-i])
          #print temp
          out_object.write(' '+atom_syb[i+1]+'  ')
          if float(temp[3])<0:
            out_object.write('%.6f' % float(temp[3]))
            out_object.write('  ')
          else:
            out_object.write(' ')
            out_object.write('%.6f' % float(temp[3]))
            out_object.write('  ')
          if float(temp[4])<0:
            out_object.write('%.6f' % float(temp[4]))
            out_object.write('  ')
          else:
            out_object.write(' ')
            out_object.write('%.6f' % float(temp[4]))
            out_object.write('  ')
          if float(temp[5])<0:
            out_object.write('%.6f' % float(temp[5]))
            out_object.write('  ')
          else:
            out_object.write(' ')
            out_object.write('%.6f' % float(temp[5]))
            out_object.write('  ')
          out_object.write('\n')

  #parse *.xyz file to obtain SMILES
  def parse_xyz(fname):
    with open(fname,'r') as in_object:
      lines = in_object.readlines()
      temp = lines[-2]
      temp = temp.split()
      return temp[0]

  #parse gaussian output files
  def parse_logfile(self):
    for dirs in os.listdir(self.root_dir):
      molecular_dir = self.root_dir + dirs + '/'
      molsfile = self.root_dir+dirs+'/'+dirs+'.mols'
      if not os.path.isfile(molsfile):
        fname = molecular_dir+dirs+'.xyz'
        smiles = parse_xyz(fname)
      
      
        work_dir = molecular_dir+'s0/'
        os.system('cd '+work_dir)
        for files in os.listdir(work_dir):
          if re.match(r'.*\.log',files):
            fname = files
            break
        if re.match(r'.*\.log',fname):
          temp = fname.split('_')
          out_file = molecular_dir+temp[0]+'_'+temp[1]+'.mols'
          fname = work_dir + fname
          parse_log_s0(fname)
        else:
          print molecular_dir
        
        tokens = '------------------------------Excited State S1: energy(Ha),lifetime(au),structure(Angstrom)-----------------------------\n'
        note1 = '  #S1'
        note2 = '               #S1 life'
        work_dir = molecular_dir+'/s1/'
        os.chdir(work_dir)
        for files in os.listdir(work_dir):
          if re.match(r'.*\.log',files):
            fname = files
            break
        if re.match(r'.*\.log',fname):
          fname = work_dir + fname
          parse_log_s1t1(fname,'s1')
        
        tokens = '------------------------------Excited State T1: energy(Ha),lifetime(au),structure(Angstrom)-----------------------------\n'
        note1 = '  #T1'
        note2 = '               #T1 life'
        work_dir = molecular_dir+'/t1/'
        os.chdir(work_dir)
        for files in os.listdir(work_dir):
          if re.match(r'.*\.log',files):
            fname = files
            break
        if re.match(r'.*\.log',fname):
          fname = work_dir + fname
          parse_log_s1t1(fname,'t1')

  def error_handle(self):
    desti_dir = '/home/qhuang/HzwDb/gdb_error/'
    n=0
    for dirs in os.listdir(self.root_dir):
      molsfile = self.root_dir+'/'+dirs+'/'+dirs+'.mols'
      dirs = self.root_dir+'/'+dirs
      if not os.path.isfile(molsfile):
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





