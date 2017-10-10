#/usr/bin/python
import os
def calculateG09(input_file,output_file):
    out_filename = input_file.split('.')
    temp = output_file.split('/')
    print input_file
    fname = out_filename[0]+'-'+temp[-1]+'.log'
    print fname
    os.environ['filename']=str(input_file)
    os.system("g09 < $filename >"+fname)
    process = os.popen("grep 'Error termination' "+fname)
    errorinfo = process.read()
    process.close()
    #import pdb 
    #pdb.set_trace()
    if errorinfo:
        print errorinfo
    if temp[-1]=='s0':
      import parselogs0
      parselogs0.parseLog(fname)
def findInputFile(rootDir):
    import re
    for files in os.walk(rootDir):
        #print files[0]
        #print files[1]
        #print files[2]
        for name in files[2]:
            if re.match(r'.*\.com',name,flags=0):
                #print name
                os.chdir(files[0])
                calculateG09(name,files[0])

findInputFile("/home/qhuang/HzwDb/gdb/000003_H2O/")
