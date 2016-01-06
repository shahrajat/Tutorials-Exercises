#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys                                                                                                        
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def get_special_files(directories):
  sp_filepaths = []
  for directory in directories:
      filenames = os.listdir(directory)
      #filenames = [item for sublist in filenames for item in sublist]
      for filename in filenames:
        #check if the pattern exists in the filename
        if re.search(r'__\w+__',filename):
          path = os.path.join(directory, filename)
          sp_filepaths.append(os.path.abspath(path))
  return sp_filepaths

#copies the files to the directory
def copy_files(todir, filepaths):
  if not os.path.exists(todir):
    os.mkdir(todir)
  for filepath in filepaths:
    shutil.copy(filepath, os.path.abspath(todir))
  return

#zips the list of files to given zip files
def zip_files(tozip, todir):
  cmd = 'zip -j '+ tozip + ' ' +  ' '.join(get_special_files(todir))
  print cmd
  (status, output) = commands.getstatusoutput(cmd)
  print output

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  directories = args 
  sp_filepaths = get_special_files(directories)
  
  if todir:
    copy_files(todir,sp_filepaths)
  
  if tozip:
    zip_files(tozip, args[0])
  
if __name__ == "__main__":
  main()
