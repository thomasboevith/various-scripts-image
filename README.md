# various-scripts-image
Scripts for all sorts of image-related purposes

## crop_resize_annotate_images

    crop_resize_annotate_images.py 0.1

    Usage:
      crop_resize_annotate_images.py [-f] [-c <string>] [-r <num>] [-A | -a <string>] [-s <num>] [-v ...] <infile> <outfile>
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
      -v                      Print info (-vv for debug info (debug).

    Examples:
      crop_resize_annotate_images.py -c '256x512+32+64' -r 800 -a 'Titel' -s 16 <infile> <outfile>
      crop_resize_annotate_images.py -c '256x512+32+64' -A -s 32 input20160607_1616.jpg output.jpg
