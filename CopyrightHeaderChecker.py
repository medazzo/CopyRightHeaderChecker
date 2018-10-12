#!/usr/bin/python

import os
import time
import ntpath
import sys
import json
from os.path import join, getsize
from shutil import copyfile
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
behaviour = """{
  "reporting": true ,
  "updatefiles": true ,
  "shebang": 
  {
    "she":["#!/","!#/bin","!#/usr/bin"],
    "check": true
  },
  "oldCopyright":
  {
    "lookforandwarn": true,
    "forceNewCopyright": false,
    "numberofline":6
  },
  "checks":
   [ 
     {
        "brief":"C/C++ Code",
        "extentions":[".c",".cpp",".h",".hpp"],
        "names":[],
        "copyright":[
          "/// @author your Comparny , Address, Country",
          "/// ",
          "/// @copyright year Company Name",
          "/// All rights exclusively reserved for company Name,",
          "/// unless otherwise expressly agreed",
          ""]
     },
      {
        "brief":"bash/scripting Code",
        "extentions":[".conf",".conf.sample",".bb",".inc",".service",".sh",".cfg",".m4" ,".init",".py",".pl"],
        "names":["init","run-ptest","llvm-config","corbos-build-env-set","corbos-init-build-env","corbos-setup-build-env","Dockerfile"],
        "copyright":[
          "# @author your Comparny , Address, Country",
          "#",
          "# @copyright  year Company Name",
          "# All rights exclusively reserved for company Name,",
          "# unless otherwise expressly agreed",
          ""]
     },
     {
       "brief":"html/js Code",
        "extentions":[".html",".js"],
        "names":[],
        "copyright":[
          "<!-- @author your Comparny , Address, Country                               -->",
          "<!--                                                                        -->",
          "<!-- @copyright  year Company Name                                          -->",
          "<!-- All rights exclusively reserved for company Name,                       -->",
          "<!-- unless otherwise expressly agreed                                      -->",
          ""]
     },
     {
       "brief":"Markdown Code",
        "extentions":[".md"],
        "names":[],
        "copyright":[
          "[comment]: <> (@author your Comparny , Address, Country                       )",
          "[comment]: <> (                                                               )",
          "[comment]: <> (@copyright  year Company Name                                  )",
          "[comment]: <> (All rights exclusively reserved for company Name,              )",
          "[comment]: <> (unless otherwise expressly agreed                              )",
          ""]
     }
    ]
}"""

# Define 
Debug = False
Outputfolder=""
excludeDirs =['.git','.repo']
Rbehaviour = json.loads(behaviour)
filesAlreadyCopyright = []
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Find all concerned Files
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def FindFiles(rootfolder ):
  """ this functions will find files as defined up """
  start = time.time()
  for bhv in Rbehaviour["checks"]: 
    bhv["files"]=[]    
  for root, dirs,files in os.walk(rootfolder):
    dirs[:] = [d for d in dirs if d not in excludeDirs]
    for x in files :      
      sfileN = os.path.join(root, x)
      if Debug : print " ==>  Checking file -->",sfileN
      #  check old copyright
      if Rbehaviour["oldCopyright"]["lookforandwarn"]:
        if checkfileCopyright(sfileN):
          filesAlreadyCopyright.append(sfileN)
          if not Rbehaviour["oldCopyright"]["forceNewCopyright"]: 
            break
      # checks
      found = False
      for bhv in Rbehaviour["checks"]:       
        # Check if file is in names
        try:
          bhv["names"].index(x)
        except :
          # Check if file is in extensions
          if Debug : print bhv["brief"]," extentions  ==>  Checking file -->",x
          for ext in bhv["extentions"] :
            if x.endswith(ext):
              bhv["files"].append(sfileN)
              if Debug : print bhv["brief"]," >> ", ext," extentions ==>  Found file -->",x 
              found = True
              break
        else:
          bhv["files"].append(sfileN)
          found = True
          if Debug : print bhv["brief"],"  names ==>  Found file -->",x    
        if found:
          break
  end = time.time()
  took = end - start  
  if(Rbehaviour["reporting"]):
    print " = = = = Analyse ",bhv['brief']," took  %.4f sec  = = = = "% took    
    for bhv in Rbehaviour["checks"]:      
      print " = = = =    ",len(bhv["files"]),"            ",bhv["brief"]," files." 
    if Rbehaviour["oldCopyright"]["lookforandwarn"]:
      print " = = = =  ! ",len(filesAlreadyCopyright)," files are already with a Copyright Headers :",filesAlreadyCopyright
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# for Sfiles check shebang 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def checkfileShebang(filename):
  """ return true if file has a shebang """
  if Rbehaviour["shebang"]["check"]:
    if Debug : print "  Will check shebang  .. " 
    infile = open(filename, 'r')
    firstLine = infile.readline()
    infile.close()    
    for she in Rbehaviour["shebang"]["she"]:
      if Debug : print "??  did file ",filename," start with ",she ," [",firstLine,"] " 
      if firstLine.startswith(she):        
        return True    
  return False
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# To check if file contain already a License Copyright Header
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def checkfileCopyright(filename):
  """ return true if file has already a Copyright in first X lines  """
  infile = open(filename, 'r')
  for x in xrange(6):
    x = x 
    line = infile.readline()    
    if "Copyright" in line or "copyright" in line:
      return True
  return False
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Apply new Copyright to a file
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ApplyCopyright( srcfile, dstfile , copyright):
  """ will apply new Copyright on dst file then append the old src file """  
  if(srcfile != dstfile):
    # create dir file if not exist
    nbase = os.path.dirname(dstfile)
    if not os.path.exists(nbase):
      os.makedirs(nbase)
    dst = open(dstfile, "w")
  else:
    tmp = "/tmp/tmp-fheadercopyrightLicense" 
    dst = open(tmp, "w")
  isSheb = checkfileShebang(srcfile)
  src = open(srcfile, "r")
  if isSheb:    
    line = src.readline()    
    dst.write(line)
    for cop in  copyright:
      dst.write(cop)
      dst.write('\n')
    # continue copy src file
    while line:       
      line = src.readline()
      dst.write(line)    
  else:
    if Debug : print " \t ==>  file  ",srcfile," DONT have shebang !"  
    for cop in  copyright:
      dst.write(cop)
      dst.write('\n')
    dst.write(src.read())
  dst.close() 
  src.close()
  if(srcfile == dstfile):
    copyfile(tmp, dstfile)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# To apply new Copyright  headers in files 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ApplyInTmp(OutDir):
  """ will apply new Copyright on array of files into OutDir with Same tree as original  """
  global Outputfolder
  # checks
  for bhv in Rbehaviour["checks"]: 
    start = time.time()   
    for x in bhv["files"] :       
      # fix folder 
      p = os.path.dirname(x)
      while p.startswith('../'): 
        p = p[3:]
      if p.startswith('/'):
        p  = p[1:]
      Outputfolder = OutDir+"/"+p
      nfile = Outputfolder+"/"+ntpath.basename(x)
      ApplyCopyright(x, nfile, bhv["copyright"])
    end = time.time()
    took = end - start 
    if(Rbehaviour["reporting"]):
      print " = = = = Applying ",bhv['brief']," took  %.4f sec  = = = = "% took
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# To apply new Copyright  headers in files 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ApplyIn():
  """ will apply new Copyright on array of files into original Dir"""
  # checks
  for bhv in Rbehaviour["checks"]: 
    start = time.time()   
    for x in bhv["files"] :
      ApplyCopyright(x, x, bhv["copyright"])
    end = time.time()
    took = end - start 
    if(Rbehaviour["reporting"]):
      print " = = = = Applying ",bhv['brief']," took  %.4f sec  = = = = "% took
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # M A I N # # # # # # # # # # # # # # # # # #  
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print " = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
print "   = = = = = = = = = = =   Copyright Header  = = = = = = = = = = = =   "
print " = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
print " "
if(not Rbehaviour["updatefiles"]):
  if len(sys.argv) != 3 :
    print " = = =  Bad parameter number !! => ",len(sys.argv)-1," instead of 2  = = = "
    print " = = =   parameter are folder source code src and folder destination  = = = "
    print " = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
    exit(-1)
else:
  if len(sys.argv) != 2 :
    print " = = =  Bad parameter number !! => ",len(sys.argv)-1," instead of 2  = = = "
    print " = = =   parameter are folder source TO BE MODIFIYED in  = = = "
    print " = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
    exit(-1)


if not os.path.exists(sys.argv[1]):
  print " = = =  Bad parameter  !! => ",sys.argv[1],"   = = = "
  print " = = =   folder source did not exist !  = = = "
  print " = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
  exit(-2)

if(not Rbehaviour["updatefiles"]):
  if os.path.exists(sys.argv[2]):
      print " = = =  Bad parameter  !! => ",sys.argv[2],"   = = = "
      print " = = =   folder destination already exist !  = = = "
      print " = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
      exit(-2)

print " = = = To modify behaviour please edit the script ",sys.argv[0]," = = = "
print " = = = Will use src Folder ",sys.argv[1]," = = = = "
if(not Rbehaviour["updatefiles"]):
  print " = = =  and put modifyied code in dst ",sys.argv[2]," = = = = "
else:
  print " = = =  and update file  inside it    = = = = "

FindFiles(sys.argv[1])
if(not Rbehaviour["updatefiles"]):
  ApplyInTmp(sys.argv[2])
else:
  ApplyIn()

print " = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
print " = = = = = = = = = = = = = = =  Done  = = = = = = = = = = = = = = = = "
if(not Rbehaviour["updatefiles"]):
  print " @  ", Outputfolder," = "
print " = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # D O N E # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
