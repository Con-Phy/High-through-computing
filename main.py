#!/usr/bin/python
from gaussianjobcontrol import GaussianJobControl

cores = '1'
cpu_cores = 16
user = 'qhuang'

root_dir = '/home/qhuang/HzwDb'
gdb = '/home/qhuang/HzwDb/gdb'
gdb_done = '/home/qhuang/HzwDb/gdb_done'
gdb_error = '/home/qhuang/HzwDb/gdb_error'

mosfile_dir = '/home/qhuang/HzwDb/molsfile'

my_gaussian = GaussianJobControl(cores,cpu_cores,user,root_dir,gdb,gdb_done,gdb_error,mosfile_dir)

#my_gaussian.error_handle()
my_gaussian.submission_control()
while True:
  for mol_dir in my_gaussian.all_mol_dir():
    #print(mol_dir)
    #print(my_gaussian.calculation_is_checked(mol_dir))
    if my_gaussian.calculation_is_checked(mol_dir):
      my_gaussian.error_handle(mol_dir)
      my_gaussian.parse_logfile(mol_dir)
      my_gaussian.mv2gdb_done(mol_dir) 
  if my_gaussian.job_is_done():
    break
  my_gaussian.my_sleep()
