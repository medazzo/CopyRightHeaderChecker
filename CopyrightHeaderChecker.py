#!/usr/bin/python
# @author Mohamed Azzouni , Paris, France
#

import os
import time
import ntpath
import sys
import json
import argparse
from os.path import join, getsize
from shutil import copyfile

behaviour = """{
  "reporting": true ,
  "updatefiles": true ,
  "excludeDirs" :[".git",".repo"],
  "shebang": 
  {
    "she":["#!/","#!/bin","#!/usr/bin"],
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
        "extensions":[".c",".cpp",".h",".hpp"],
        "names":[],
        "copyright":[
          "/// @author your $$CompanyName$$ , $$CompanyAddress$$, $$CompanyCountry$$",
          "/// ",
          "/// @copyright $$CompanyYear$$ $$CompanyName$$",
          "/// All rights exclusively reserved for $$CompanyName$$,",
          "/// unless otherwise expressly agreed",
          ""]
     },
      {
        "brief":"bash/scripting Code",
        "extensions":[".conf",".conf.sample",".bb",".inc",".service",".sh",".cfg",".m4" ,".init",".py",".pl"],
        "names":["init","run-ptest","llvm-config","build-env-set","init-build-env","setup-build-env","Dockerfile"],
        "copyright":[
          "# @author your $$CompanyName$$ , $$CompanyAddress$$, $$CompanyCountry$$",
          "#",
          "# @copyright  $$CompanyYear$$ $$CompanyName$$",
          "# All rights exclusively reserved for $$CompanyName$$,",
          "# unless otherwise expressly agreed",
          ""]
     },
     {
       "brief":"html/js Code",
        "extensions":[".html"],
        "names":[],
        "copyright":[
          "<!-- @author your $$CompanyName$$ , $$CompanyAddress$$, $$CompanyCountry$$                               -->",
          "<!--                                                                        -->",
          "<!-- @copyright  $$CompanyYear$$ $$CompanyName$$                                           -->",
          "<!-- All rights exclusively reserved for $$CompanyName$$ ,                      -->",
          "<!-- unless otherwise expressly agreed                                      -->",
          ""]
     },
     {
       "brief":"Markdown Code",
        "extensions":[".md"],
        "names":[],
        "copyright":[
          "[comment]: <> (@author your $$CompanyName$$ , $$CompanyAddress$$, $$CompanyCountry$$                       )",
          "[comment]: <> (                                                               )",
          "[comment]: <> (@copyright  $$CompanyYear$$ $$CompanyName$$                                  )",
          "[comment]: <> (All rights exclusively reserved for $$CompanyName$$,              )",
          "[comment]: <> (unless otherwise expressly agreed                              )",
          ""]
     }
    ]
}"""

# Define 
Debug = False
Outputfolder=""
Rbehaviour = json.loads(behaviour)
filesAlreadyCopyright = []

# Parameters : 

# --dumpShebang           :               : dump the current list of managed shebang
# --dumpExtension         :               : dump the current list of managed files extensions

# -r --report              [default: False]: if true print a complete report for what has done 
# -u --update              [default: False]: if true files will be updated else a modified copy will be generated
# -w --warnOldHeader       [default: False]: if true  do warn about Old Header existant in files in traces
# -f --forceOldHeader      [default: False]: if true do replace old header if exist (exclusif with option warnOldHeader ) 

# -n --nameCompany         :               : string
# -a --adressCompany       :               : string
# -c --countryCompany      :               : string
# -y --yearCompany         :               : string


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Find all concerned Files
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def SetupParserParameter( ):
  """ this functions will setup parameter and parser for argument"""
  parser = argparse.ArgumentParser(description='Checks sources code files for Copyright Header and add ours.',
                        prog='CopyrightHeaderChecker')
  parser.add_argument('--version', action='version', version='%(prog)s 1.0')
  parser.add_argument('--verbose', action='store_true', help='verbose mode ')
  subparsers = parser.add_subparsers(help='sub command :')
  parser_info = subparsers.add_parser('info', help='get checker informations ')
  parser_info.add_argument('-s','--dumpShebang',  dest='dumpShebang',action='store_true',
                       help='dump the current list of managed shebang')
  parser_info.add_argument('-e', '--dumpExtension',  dest='dumpExtension',action='store_true',
                       help='dump the current list of managed files extensions')
  parser_process = subparsers.add_parser('process', help='process checker')
  parser_process.add_argument('-r','--report',  dest='report',action='store_true',
                       help='print a detailled report for what has done')
  parser_process.add_argument('-u','--update',  dest='update',action='store_true',
                       help='update files in sources path')
  parser_process.add_argument('-w','--warnOldHeader',  dest='warnOldHeader',action='store_false',
                       help='warn about Old Header existant in files in traces ')
  parser_process.add_argument('-f','--forceOldHeader',  dest='forceOldHeader',action='store_true',
                       help='replace old header if exist in files ')
  parser_process.add_argument('-n','--nameCompany',  dest='nameCompany',required=True,
                       help='company name to be used in copyright header')
  parser_process.add_argument('-a','--adressCompany',  dest='adressCompany',required=True,
                       help='company address to be used in copyright header')
  parser_process.add_argument('-c','--countryCompany',  dest='countryCompany',required=True,
                       help='company country to be used in copyright header')
  parser_process.add_argument('-y','--yearCompany',  dest='yearCompany',required=True,
                       help='years to be used in copyright header ')
  parser_process.add_argument('-i','--inputSourecCodeFolder',  dest='inputFolder',required=True,
                       help='path to folder containing source code to operate on')
  args = parser.parse_args()
  return args

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Find all concerned Files
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def FindFiles(rootfolder, report ):
  """ this functions will find files as defined up """
  start = time.time()
  for bhv in Rbehaviour["checks"]: 
    bhv["files"]=[]    
  for root, dirs,files in os.walk(rootfolder):
    dirs[:] = [d for d in dirs if d not in Rbehaviour["excludeDirs"]]
    for x in files :      
      sfileN = os.path.join(root, x)
      if Debug : print(' ==>  Checking file --> {}', format(sfileN))
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
          if Debug : 
            print bhv["brief"],"  extensions  ==>  Checking file --> ",  
            for x in bhv["extensions"]:
              print  x,
            print " "
          for ext in bhv["extensions"] :
            if x.endswith(ext):
              bhv["files"].append(sfileN)
              if Debug : 
                print bhv["brief"]," >> ",ext," extensions ==>  Found file --> ",x
              found = True
              break
        else:
          bhv["files"].append(sfileN)
          found = True
          if Debug : print ("{} names ==>  Found file -->",format(bhv["brief"],x))
        if found:
          break
  end = time.time()
  took = end - start  
  if(report):
    print "  - - - - - - Analyse ",bhv['brief']," took  %.4f sec  - - - - - - "% took 
    for bhv in Rbehaviour["checks"]:      
      print "  - - - - - -    ",len(bhv["files"]),"            ",bhv["brief"]," files." 
    if (Rbehaviour["oldCopyright"]["lookforandwarn"]):
      print "  - - - - - -  	! ",len(filesAlreadyCopyright)," files are already with a Copyright Headers :"
      for x in filesAlreadyCopyright:
       print  "   - ",x

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# for Sfiles check shebang 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def checkfileShebang(filename):
  """ return true if file has a shebang """
  if Rbehaviour["shebang"]["check"]:
    if Debug : print("  Will check shebang  .. " )
    infile = open(filename, 'r')
    firstLine = infile.readline()
    infile.close()    
    for she in Rbehaviour["shebang"]["she"]:
      if Debug : print("??  did file ",filename," start with ",she ," [",firstLine,"] " )
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
def ApplyCopyright( srcfile, dstfile , copyright, cname, ccontry, caddress, cyear):
  """ will apply new Copyright on dst file then append the old src file """ 
  # apply comany information 
  copyright = [w.replace('$$CompanyName$$', cname) for w in copyright]
  copyright = [w.replace('$$CompanyCountry$$', ccontry) for w in copyright]
  copyright = [w.replace('$$CompanyAddress$$', caddress) for w in copyright]
  copyright = [w.replace('$$CompanyYear$$', cyear) for w in copyright]
 
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
    if Debug : print(" \t ==>  file  ",srcfile," DONT have shebang !"  )
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
def ApplyInTmp(OutDir,report, cname, ccontry, caddress, cyear):
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
      ApplyCopyright(x, nfile, bhv["copyright"], cname, ccontry, caddress, cyear)
    end = time.time()
    took = end - start 
    if(report):
      print "  - - - - - - Applying ",bhv['brief']," took  %.4f sec  - - - - - - "% took

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# To apply new Copyright  headers in files 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ApplyIn(report, cname, ccontry, caddress, cyear):
  """ will apply new Copyright on array of files into original Dir"""
  # checks
  for bhv in Rbehaviour["checks"]: 
    start = time.time()   
    for x in bhv["files"] :
      ApplyCopyright(x, x, bhv["copyright"], cname, ccontry, caddress, cyear)
    end = time.time()
    took = end - start 
    if(report):
      print"  - - - - - - Applying ",bhv['brief']," took  %.4f sec  - - - - - - "% took

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # M A I N # # # # # # # # # # # # # # # # # #  
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
print("- - - - - - - - - - - - - - - - - -   Copyright Header  - - - - - - - - - - - - - - - - - - - - -")
args = SetupParserParameter()
Debug = args.verbose
if "dumpShebang" in args: 
  print("- - - - - - -  Info  - - - - - - ->")
  if(args.dumpShebang == True):
    print "     Supportted shebang: ", 
    for x in Rbehaviour["shebang"]["she"]:
      print  x,
    print " "
  if(args.dumpExtension == True):
    print "     Supportted Extensions: "
    for bhv in Rbehaviour["checks"]: 
      print "      ",     
      print bhv["brief"],"   : ",  
      for x in bhv["extensions"]:
        print  x,
      print " "
else:
  if not os.path.exists(args.inputFolder):
    print("   - - -  Bad parameter , source code path  !! => ",args.inputFolder)
    print("   - - -   folder source did not exist !  - - - ")
    exit(-2)
  print("- - - - - - -  Analyse  - - - - - - ->")
  FindFiles(args.inputFolder, args.report)
  print("- - - - - - -  Process  - - - - - - ->")
  if ( args.update == True):
    ApplyIn(args.report,args.nameCompany, args.countryCompany, args.adressCompany, args.yearCompany)
  else:
    ApplyInTmp("/tmp", args.report, args.nameCompany, args.countryCompany, args.adressCompany, args.yearCompany)
  print "     Generated   ", Outputfolder
print("<- - - - - - - Done - - - - - - - - - -")
print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # D O N E # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
