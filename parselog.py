#/usr/bin/python
import re
import os
import sys     
def parseLogS0(fname):
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
      res_list.append(i)
  if res_list2:
    temp = str1.findall(res_list2[-1])
    res_list.append(temp[-1])
  if res_list3:
    temp = str1.findall(res_list3[-1])
    res_list.append(temp[-1])
  if res_list4:
    temp = str1.findall(res_list4[-4])
    res_list.append(temp[-1])
  if res_list5:
    temp = str1.findall(res_list4[-3])
    res_list.append(temp[0])
    lumo = float(res_list[-1])
    homo = float(res_list[-2])
    res_list.append(lumo-homo)
  if res_list5:
    temp = str1.findall(res_list5[-1])
    res_list.append(temp[-1])
  if res_list6:
    temp = str1.findall(res_list6[-1])
    res_list.append(temp[-1])
  if res_list7:
    temp = str1.findall(res_list7[-1])
    res_list.append(temp[-1])
  if res_list8:
    temp = str1.findall(res_list8[-1])
    res_list.append(temp[-1])
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
        print i
        temp = i.split(' ')
        for j in temp:
          out_object.write(' ')
          out_object.write('%.6f' % float(j))
          out_object.write('  ')
        out_object.write('\n')
    out_object.write('------------------------------Vibration Modes---------------------------------------------------------------------------\n')
    if vibration:
      for i in vibration:
        for j in i:
          #out_object.write(' ')
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
  #
    #out_object.write('------------------------------Excited State T1: energy(Ha),lifetime(au),structure(Angstrom)-----------------------------\n')
  
    #out_object.write('------------------------------Emitting Efficiency-----------------------------------------------------------------------\n')
  #    out_object.write('------------------------------Emitting Spectrum (cm-1,au)---------------------------------------------------------------\n')
  
  #   out_object.write('------------------------------Absorption Spectrum (cm-1,au)-------------------------------------------------------------\n')
  
  #  out_object.write('------------------------------End---------------------------------------------------------------------------------------\n')

def parseLogS1T1(fname):
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

def parseXyz(fname):
  with open(fname,'r') as in_object:
    lines = in_object.readlines()
    temp = lines[-2]
    temp = temp.split()
    return temp[0]


root_dir = '/home/qhuang/HzwDb/gdb/'

for dirs in os.listdir(root_dir):
  molecular_dir = root_dir + dirs + '/'
  #print molecular_dir
  #print dirs
  for files in os.listdir(molecular_dir):
    if re.match(r'.*\.xyz',files):
      fname = molecular_dir+files
      break
  #print fname
  smiles = parseXyz(fname)


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
    parseLogS0(fname)
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
    parseLogS1T1(fname)
  
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
    parseLogS1T1(fname)

