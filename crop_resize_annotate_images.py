#!/usr/bin/env python2
import datetime
import docopt
import logging
import os
import re
import subprocess
import sys
import time

version = '0.1'

__doc__ = """
crop_resize_annotate_images.py {version}

Usage:
  {filename} [-f] [-c <string>] [-r <num>] [-A | -a <string>] [-s <num>]
             [-v ...] <infile> <outfile>
  {filename} (-h | --help)
  {filename} --version

Options:
  -c <string>             Crop image geometry.
  -r <num>                Output image width.
  -a <string>             Annotation string.
  -A                      Annotate with ISO date from filename.
  -s <num>                Font size [default: 32].
  -f --forceoverwrite     Overwrite output files.
  -h, --help              Show this screen.
  --version               Show version.
  -v                      Print info (-vv for debug info (debug)).

Examples:
  {filename} -c '256x512+32+64' -r 800 -a 'Titel' -s 16 <infile> <outfile>
  {filename} -c '256x512+32+64' -A -s 32 input20160607_1616.jpg output.jpg

Copyright (C) 2016 Thomas Boevith

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

    cmd = ['convert']
    if args['-c']:
        cmd.append('-crop')
        cmd.append(args['-c'])
        cmd.append('+repage')

    if args['-r']:
        cmd.append('-resize')
        cmd.append(args['-r'])
        cmd.extend('-filter point -interpolate NearestNeighbor'.split())

    cmd.append(args['<infile>'])

    if os.path.isfile(args['<outfile>']):
        if not args['--forceoverwrite']:
            log.warning('Outfile already exists: %s.' % args['<outfile>'])
            log.warning('Skipping. Use -f, --forceoverwrite to overwrite')
            sys.exit(1)
        else:
            log.info('Overwriting file because -f, --forceoverwrite set.')

            if args['-A']:
                timestamp_patterns = [re.compile(r'\d{12}'),
                                      re.compile(r'\d{8}_\d{4}'),
                                      re.compile(r'\d{8}_\d{6}')]
                timestamp_formats = ['%Y%m%d%H%M', '%Y%m%d_%H%M',
                                     '%Y%m%d_%H%M%S']
                for timestamp_pattern, timestamp_format in \
                        zip(timestamp_patterns, timestamp_formats):
                    match = timestamp_pattern.findall(args['<infile>'])
                    if match != []:
                        annotationstring = \
                            datetime.datetime.strptime(match[0],
                                timestamp_format).strftime('%Y-%m-%d %H:%M')
                        break

            elif args['-a']:
                annotationstring = args['-a']

            if args['-A'] or args['-a']:
                cmd.extend("-background White".split())
                cmd.append("-pointsize")
                cmd.append(args['-s'])
                cmd.append("label:" + annotationstring)
                cmd.extend("+swap -gravity Center -append".split())

    cmd.append(args['<outfile>'])
    log.debug(cmd)

    log.info('Running command in subprocess: %s' % cmd)
    (out, err) = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()

    log.debug('Processing time={0:.2f} s'.format(time.time() - start_time))
    log.debug('%s ended' % os.path.basename(__file__))
