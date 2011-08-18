# -*- coding: utf-8 -*-
import os, os.path, shutil
import sys

YUI_COMPRESSOR = 'yuicompress/yuicompressor-2.4.6.jar'

def compress(in_files, out_file, in_type='js', verbose=False,
             temp_file='.temp'):
    temp = open(temp_file, 'w')
    for f in in_files:
        fh = open(f)
        data = fh.read() + '\n'
        fh.close()

        temp.write(data)

        print ' + %s' % f
    temp.close()

    options = ['-o "%s"' % out_file,
               '--type %s' % in_type]

    if verbose:
        options.append('-v')

    os.system('java -jar "%s" %s "%s"' % (YUI_COMPRESSOR,
                                          ' '.join(options),
                                          temp_file))

    org_size = os.path.getsize(temp_file)
    new_size = os.path.getsize(out_file)

    print '=> %s' % out_file
    print 'Original: %.2f kB' % (org_size / 1024.0)
    print 'Compressed: %.2f kB' % (new_size / 1024.0)
    print 'Reduction: %.1f%%' % (float(org_size - new_size) / org_size * 100)
    print ''

    os.remove(temp_file)
    
SCRIPTS = [
      'src/static/js/jquery.min.js',
      'src/static/js/jquery-ui-1.8.7.custom.min.js',
      'src/static/js/jquery.addplaceholder.js',
      'src/static/js/swfupload.js',
      'src/static/js/plugins/swfupload.cookies.js',
      'src/static/js/jquery.ketchup.js',
      'src/static/js/backend.js',
    ]

SCRIPTS_OUT_DEBUG = 'backend-debug.js'

STYLESHEETS = [
    'src/static/css/common.css',
    'src/static/css/backend.css',
    'src/static/css/fb-buttons.css',
    ]

def main():

  if len(sys.argv) < 2:
    print 'PONELE VERSION PUTO'
    return
    
  version = sys.argv[1]  

  SCRIPTS_OUT       = 'backend.min-%s.js' % version
  STYLESHEETS_OUT = 'backend.min-%s.css' % version

  print 'Compressing JavaScript...'
  compress(SCRIPTS, SCRIPTS_OUT, 'js', False, SCRIPTS_OUT_DEBUG)

  print 'Compressing CSS...'
  compress(STYLESHEETS, STYLESHEETS_OUT, 'css')

if __name__ == '__main__':
  main()