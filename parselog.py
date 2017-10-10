#/usr/bin/python
def writeMols(molecular,charge,number,res_list,atom_num,atom_pos,atom_syb,mulliken,atom_mass,frequencies,vibration):
  import re
  out_file = number+'_'+molecular+'.mols'
  with open(out_file,'w') as out_object:
    out_object.write('------------------------------Chemical Formula and Charge---------------------------------------------------------------\n')
    out_object.write(' ')
    out_object.write(molecular+'  '+charge+'\n')
    out_object.write('------------------------------SMILES------------------------------------------------------------------------------------\n')
    out_object.write(' H2O\n')
    out_object.write('------------------------------Basic properties--------------------------------------------------------------------------\n')
    out_object.write('--tag--index---A---B---C----dipole--isotropic--homo--lumo--gap--r2------zpve--U0--U--H--G--Cv---------------------------\n')
    out_object.write('--xxx--XXXXXX--GHz-GHz-Ghz--Debye---Bohr^3-----Ha----Ha----Ha---Bohr^2--Ha----Ha--Ha-Ha-Ha-cal/(mol K)------------------\n')
    out_object.write(' gdb  '+number+'  ')
    for i in res_list:
      out_object.write('%.6f' % float(i))
      out_object.write('  ')
    out_object.write('\n')
    out_object.write('------------------------------Element,XYZ (Angstrom)--------------------------------------------------------------------\n')
    temp = str(atom_num)
    out_object.write(' '+temp+'\n')
    str1 = re.compile(r'-*\d+\.*\d*')
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
    for i in mulliken:
      out_object.write(' ')
      out_object.write('%.6f' % float(i))
      out_object.write('  ')
    out_object.write('\n')
    out_object.write('------------------------------Atom Mass (Relative atomic mass)----------------------------------------------------------\n')
    for i in atom_mass:
      out_object.write(' ')
      out_object.write('%.6f' % float(i))
      out_object.write('  ')
    out_object.write('\n')
    out_object.write('------------------------------Vibration Frequency (cm-1)----------------------------------------------------------------\n')
    for i in frequencies:
      i=i.rstrip()
      temp = i.split(' ')
      for j in temp:
        out_object.write(' ')
        out_object.write('%.6f' % float(j))
        out_object.write('  ')
      out_object.write('\n')
    out_object.write('------------------------------Vibration Modes---------------------------------------------------------------------------\n')
    for i in vibration:
      for j in i:
        out_object.write(' ')
        for k in j:
          out_object.write('%.6f' % float(k))
          out_object.write('  ')
        out_object.write('\n')

          


def parseCom(fname):
  import re
  atom_syb = []
  temp = fname.split('.')
  fname = temp[0]+'.com'
  in_object = open(fname,'r')
  while 1:
    line = in_object.readline()
    if not line:
      break
    res = re.match(r'[0-9]\s*[0-9]',line)
    if res:
      temp = line.split(' ')
      atom_syb.append(temp[0])
    res = re.match(r'[^0-9]((\s*)(-*)([0-9]+(\.+)[0-9]*)(.*)){3}',line)
    if res:
      temp = line.split(' ')
      atom_syb.append(temp[0])
  in_object.close()
  return atom_syb
  
def parseLog(fname):
  atom_syb = parseCom(fname)
  charge = atom_syb[0]
  atom_num = len(atom_syb)-1
  temp = fname.split('_')
  molecular = temp[1]
  number = temp[0]
  import re
  temp = []
  mulliken = []
  atom_pos = []
  atom_mass = []
  frequency = ''
  frequencies = []
  vibration = []
  res_list = []
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
        res_list15 = []
        str1 = re.compile(r'-*\d+\.\d+')
        temp = str1.findall(line)
        for i in temp:
           frequency =i+' '+frequency
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
          temp_list.append(temp[0])
          temp_list.append(temp[1])
          temp_list.append(temp[2])
          temp_list1.append(temp_list)
          temp_list = []
          temp_list.append(temp[3])
          temp_list.append(temp[4])
          temp_list.append(temp[5])
          temp_list2.append(temp_list)
          temp_list = []
          temp_list.append(temp[6])
          temp_list.append(temp[7])
          temp_list.append(temp[8])
          temp_list3.append(temp_list)
          j+=1
        vibration.append(temp_list1)
        vibration.append(temp_list2)
        vibration.append(temp_list3)
        print vibration
        
      res = re.match(r'.*Temperature',line)
      if res:
        j = 0
        while j < atom_num:
          line = in_object.readline()
          res_list14.append(line)
          j+=1
        
  for i in range(atom_num):
    atom_pos.append(res_list12[-1-i])
  str1 = re.compile(r'-*\d+\.\d+')
  temp = str1.findall(res_list1[-1])
  for i in temp:
    res_list.append(i)
  temp = str1.findall(res_list2[-1])
  res_list.append(temp[-1])
  temp = str1.findall(res_list3[-1])
  res_list.append(temp[-1])
  temp = str1.findall(res_list4[-4])
  res_list.append(temp[-1])
  temp = str1.findall(res_list4[-3])
  res_list.append(temp[0])
  lumo = float(res_list[-1])
  homo = float(res_list[-2])
  res_list.append(lumo-homo)
  temp = str1.findall(res_list5[-1])
  res_list.append(temp[-1])
  temp = str1.findall(res_list6[-1])
  res_list.append(temp[-1])
  temp = str1.findall(res_list7[-1])
  res_list.append(temp[-1])
  temp = str1.findall(res_list8[-1])
  res_list.append(temp[-1])
  temp = str1.findall(res_list9[-1])
  res_list.append(temp[-1])
  temp = str1.findall(res_list10[-1])
  res_list.append(temp[-1])
  temp = str1.findall(res_list11[-1])
  res_list.append(temp[-2])
  for i in range(atom_num):
    temp = res_list13[-1-i].split(' ')
    mulliken.append(temp[-1])
  for i in res_list14:
    temp = i.split(' ')
    atom_mass.append(temp[-1])
  
  writeMols(molecular,charge,number,res_list,atom_num,atom_pos,atom_syb,mulliken,atom_mass,frequencies,vibration)
fname = '000003_H2O_s0.log'
parseLog(fname)
