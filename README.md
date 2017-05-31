# various-scripts-image
Scripts for all sorts of image-related purposes

## crop_resize_annotate_images

    crop_resize_annotate_images.py 0.1

    Usage:
      crop_resize_annotate_images.py [-f] [-c <string>] [-r <num>] [-A | -a <string>] [-s <num>]
                                     [-v ...] <infile> <outfile>
      crop_resize_annotate_images.py (-h | --help)
      crop_resize_annotate_images.py --version

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
      crop_resize_annotate_images.py -c '256x512+32+64' -r 800 -a 'Titel' -s 16 <infile> <outfile>
      crop_resize_annotate_images.py -c '256x512+32+64' -A -s 32 input20160607_1616.jpg output.jpg

## 2animatedgif

    2animatedgif.py 0.1 - makes animated GIF from images

    Usage:
      2animatedgif.py [-d <time>] [-F <time>] [-L <time>] [-c <num>] [-O <level>] [-l]
                 [-D] [-r] [-s <num>] [-f] [-v ...] -o <outfile> <infiles> ...
      2animatedgif.py (-h | --help)
      2animatedgif.py --version

    Options:
      -d <time>          Set frame delay (in 1/100sec) [default: 50].
      -F <time>          Set first frame delay (in 1/100sec).
      -L <time>          Set last frame delay (in 1/100sec).
      -l                 Do not loop.
      -r                 Reverse at end of sequence.
      -c <num>           Reduce number of colors to num (2-256) [default: 256].
      -D                 Dither image after changing colormap.
      -O <level>         Optimize GIF for space using level (1-3) [default: 1].
                          1 Stores only changed portion of each image (default).
                          2 Also uses transparency to shrink the file further.
                          3 Try several methods (usually slower, sometimes better).
      -s <num>           Use only every num frames.
      -o <outfile>       Write animated GIF to outfile.
      -f                 Overwrite output files.
      -h, --help         Show this screen.
      --version          Show version.
      -v                 Print info (-vv for debug info (debug)).

    Examples:
      2animatedgif.py -o out.gif -d5 -F100 -L100 -r -D -c32 -s2 img00*.png
