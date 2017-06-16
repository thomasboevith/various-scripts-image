#!/usr/bin/env python2
import datetime
import docopt
import logging
import os
import re
import shlex
import subprocess
import sys
import time

version = '0.1'

__doc__ = """
2animatedgif.py {version} - makes animated GIF from images

Usage:
  {filename} [-d <time>] [-F <time>] [-L <time>] [-c <num>] [-O <level>] [-l]
             [-D] [-r] [-s <num>] [-f] [--convertargs <args>] [-v ...] -o <outfile> <infiles> ...
  {filename} (-h | --help)
  {filename} --version

Options:
  -d <time>            Set frame delay (in 1/100sec) [default: 50].
  -F <time>            Set first frame delay (in 1/100sec).
  -L <time>            Set last frame delay (in 1/100sec).
  -l                   Do not loop.
  -r                   Reverse at end of sequence.
  -c <num>             Reduce number of colors to num (2-256) [default: 256].
  -D                   Dither image after changing colormap.
  -O <level>           Optimize GIF for space using level (1-3) [default: 3].
                        1 Stores only changed portion of each image (default).
                        2 Also uses transparency to shrink the file further.
                        3 Try several methods (usually slower, sometimes better).
  -s <num>             Use only every num frames.
  -o <outfile>         Write animated GIF to outfile.
  --convertargs <args> Additional arguments to convert.
  -f                   Overwrite output files.
  -h, --help           Show this screen.
  --version            Show version.
  -v                   Print info (-vv for debug info (debug)).

Examples:
  {filename} -o out.gif -d5 -F100 -L100 -r -D -c32 -s2 img00*.png
  {filename} -o out.gif --convertargs '-scale 256 -alpha off' img00*.png

Dependencies:
  Gifsicle (tested with Gifsicle 1.64)
  ImageMagick (convert) (tested with ImageMagick 6.6.9-7)

Copyright (C) 2017 Thomas Boevith

License: GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it. There is NO
WARRANTY, to the extent permitted by law.
""".format(filename=os.path.basename(__file__), version=version)


if __name__ == '__main__':

    start_time = time.time()
    args = docopt.docopt(__doc__, version=str(version))

    log = logging.getLogger(os.path.basename(__file__))
    formatstr = '%(asctime)-15s %(name)-17s %(levelname)-5s %(message)s'
    if args['-v'] >= 2:
        logging.basicConfig(level=logging.DEBUG, format=formatstr)
    elif args['-v'] == 1:
        logging.basicConfig(level=logging.INFO, format=formatstr)
    else:
        logging.basicConfig(level=logging.WARNING, format=formatstr)

    log.debug('%s started' % os.path.basename(__file__))
    log.debug('docopt args=%s' % str(args).replace('\n', ''))

    cmd_convert = ['convert']

    if args['-s']:
        log.debug('Skipping every %s frame' % args['-s'])
        args['<infiles>'] = args['<infiles>'][::int(args['-s'])]

    if args['-r']:
        cmd_convert.extend(reversed(args['<infiles>']))

    if args['--convertargs']:
        cmd_convert.extend(shlex.split(args['--convertargs']))

    cmd_convert.extend(args['<infiles>'])

    cmd_convert.append('GIF:-')

    cmd_gifsicle = ['gifsicle']
    cmd_gifsicle.append('--delay=%s' % args['-d'])

    if not args['-l']:
        cmd_gifsicle.append('--loop')

    if args['-c']:
        cmd_gifsicle.append('--colors=%s' % args['-c'])

    if args['-D']:
        cmd_gifsicle.append('--dither')

    cmd_gifsicle.append('--multifile')

    if os.path.isfile(args['-o']):
        if not args['-f']:
            log.warning('Outfile already exists: %s.' % args['-o'])
            log.warning('Skipping. Use -f to overwrite')
            sys.exit(1)
        else:
            log.info('Overwriting file because -f, --forceoverwrite set.')

    cmd_gifsicle.append('-')

    cmd_gifsicle.append('-o%s' % args['-o'])

    log.info("Making gif")
    log.debug("Convert/gifsicle command: %s | %s"
              % (' '.join(cmd_convert), ' '.join(cmd_gifsicle)))

    process_convert = subprocess.Popen(cmd_convert, stdout=subprocess.PIPE)
    process_gifsicle = subprocess.check_output(cmd_gifsicle,
                                               stdin=process_convert.stdout)
    process_convert.wait()

    if args['-F'] or args['-L']:
        log.info('Changing delays')
        cmd_delays = ['gifsicle']
        cmd_delays.extend(['-b', args['-o']])
        if args['-F']:
            cmd_delays.extend(['-d%s' % args['-F'], "#0"])
        if args['-L']:
            cmd_delays.extend(['-d%s' % args['-L'], "#-1"])

        process_delays = subprocess.Popen(cmd_delays, stdout=subprocess.PIPE)

    if args['-O'] == '2' or args['-O'] == '3':
        log.info('Optimizing: %s')
        cmd_optimize = ['gifsicle']
        cmd_optimize.append('-O%s' % args['-O'])
        cmd_optimize.append('%s' % args['-o'])
        process_optimize = subprocess.Popen(cmd_optimize,
                                            stdout=subprocess.PIPE)

    log.info('Final file %s of size: %s K' %
             (args['-o'], int(round(os.stat(args['-o']).st_size/1024.))))

    log.debug('Processing time={0:.2f} s'.format(time.time() - start_time))
    log.debug('%s ended' % os.path.basename(__file__))
