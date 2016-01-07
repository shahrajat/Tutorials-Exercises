#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def url_sort_key(url):
  """Used to order the urls in increasing order by 2nd word if present."""
  match = re.search(r'-(\w+)-(\w+)\.\w+', url)
  if match:
    return match.group(2)
  else:
    return url

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  #get the host name 
  underscore = filename.index('_')
  host = filename[underscore + 1:]
  
  # dict to avoid duplicates
  url_dict = dict()
  f = open(filename,'r')
  for line in f:
    # get path which follows GET.
    match = re.search(r'"GET ([^ ]+)', line)
    if match:
      path = match.group(1)
      if 'puzzle' in path:
        url_dict['http://' + host + path] = 1

  return sorted(url_dict.keys(), key=url_sort_key)

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  indexHTML = file(os.path.join(dest_dir, 'index.html'), 'w')
  indexHTML.write('<html><body>\n')

  i = 0
  for img_url in img_urls:
    local_name = 'img' + str(i)
    print('Receiving...'+ img_url)
    urllib.urlretrieve(img_url, os.path.join(dest_dir, local_name))
    #write the image tag to index.html file
    indexHTML.write('<img src="'+local_name+'">')
    i += 1

  indexHTML.write('\n</body></html>\n')
  indexHTML.close()
  
def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
