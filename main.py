#!/usr/bin/python
from gaussianjobcontrol import GaussianJobControl

flag = 0

''' 
if flag = 0, the script just handle the error and process the data
otherwise, submission,handle error and process data
'''
cores = '1'
cpu_cores = 16
user = 'qhuang'

'''
the number of cpu that every job use is set by the variable cores
the max number of cpu that machine have or jobs that user define is set by the variable cpu_cores
user name who submit the calculation jobs
'''

root_dir = '/home/qhuang/HzwDb'
gdb = '/home/qhuang/HzwDb/gdb'
gdb_done = '/home/qhuang/HzwDb/gdb_done'
gdb_error = '/home/qhuang/HzwDb/gdb_error'
molsfile_dir = '/home/qhuang/HzwDb/molsfile'

'''
all the work dirctories are included in variable root_dir
jobs in calculating are included in variable gdb
jobs done are included in variable gdb_done
jobs with error are included in variable gdb_error 
all mols files are included in variable molsfile_dir
'''

my_gaussian = GaussianJobControl(cores,cpu_cores,user,root_dir,gdb,gdb_done,gdb_error,molsfile_dir)

if flag:
  my_gaussian.submission_control()
  while True:
    for mol_dir in my_gaussian.all_mol_dir():
      if my_gaussian.calculation_is_checked(mol_dir):
        if not my_gaussian.error_handle(mol_dir):
          my_gaussian.parse_logfile(mol_dir)
          my_gaussian.mv2gdb_done(mol_dir) 
    if my_gaussian.job_is_done():
      break
    my_gaussian.my_sleep()
else:
  for mol_dir in my_gaussian.all_mol_dir():
    if not my_gaussian.error_handle(mol_dir):
      my_gaussian.parse_logfile(mol_dir)
      my_gaussian.mv2gdb_done(mol_dir)
