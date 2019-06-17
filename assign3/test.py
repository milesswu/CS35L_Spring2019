#!/usr/bin/python

import random, sys, string
import argparse
    
def main():
    prog_name=argparse._sys.argv[0]
    usage_msg="""Usage: {} [OPTION]... [FILE]
  or:  %(prog)s -e [OPTION]... [ARG]...
  or:  shuf -i LO-HI [OPTION]...
Write a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input.

Mandatory arguments to long options are mandatory for short options too.
  -e, --echo                treat each ARG as an input line
  -i, --input-range=LO-HI   treat each number LO through HI as an input line
  -n, --head-count=COUNT    output at most COUNT lines
  -r, --repeat              output lines can be repeated
      --help     display this help and exit
      --version  output version information and exit
""".format(prog_name)

    def_msg= """Try '{} --help' for more information.\n""".format(argparse._sys.argv[0])
    error_msg = {
        'extra': prog_name + ": extra operand '{}'\n",
        'invalid': prog_name + ": invalid option -- '{}'\n",
        'unrecog': prog_name + ": unrecognized option '{}'\n",
        'range': prog_name + ": invalid input range: '{}'\n",
        'line_count': prog_name + ": invalid line count: '{}'\n",
        'no_arg': prog_name + ": option requires an argument -- '{}'\n",
        'is_dir': prog_name + ": read error: Is a directory\n",
        'not_file': prog_name + ": {}: No such file or directory\n",
        'combo': prog_name + ": cannot combine {} and {} options\n",
        'no_repeat': prog_name + ": no lines to repeat\n"
    }
    parser = argparse.ArgumentParser(prog='test.py', add_help=False, usage=def_msg)
    parser.add_argument("-e", "--echo", action="store_true", dest="echo", default=False)
    parser.add_argument("--help", action="store_true", dest="show_help", default=False)
    parser.add_argument('-r', '--repeat', action="store_true", dest="repeat", default=False)
    parser.add_argument('-i', '--input-range', action="store", dest="i_range", nargs='?', const=False)
    parser.add_argument('-n', '--head-count', action="store", dest="count", #default=sys.maxsize,
                        nargs='?', const=False)
    parser.add_argument('filename', action="store", nargs='?', const=False, default='')
    options, args = parser.parse_known_args()
    print(options, args)
    filename = options.filename
    try:
        show_help = bool(options.show_help)
        if show_help:
           print(usage_msg)
    except:
        print("help")
        parser.exit(status=1, message=error_msg['invalid'].format(options.show_help))
    try:
        echo = bool(options.echo)
        if echo:
            print("Echo option active")
    except:
        print("echo")
        parser.exit(status=1, message=error_msg['invalid'].format(options.echo))
    try:
        repeat = bool(options.repeat)
        if repeat:
            print("Repeat option active")
    except:
        print("repeat")
        parser.exit(status=1, message=error_msg['invalid'].format(options.repeat))
    i_flag = options.i_range
    start = None
    end = None
    if i_flag == False:
        parser.exit(1, error_msg['no_arg'].format('i'))
    elif i_flag != None:
        print(start)
        try:
            i_range = list(options.i_range.split('-', 1))
        except:
            parser.exit(status=1, message=error_msg['range'].format(options.i_range))
        try:
            start = int(i_range[0])
            print("Range start: {}".format(start))
        except:
            parser.exit(status=1, message=error_msg['range'].format(i_range[0]))
        try:
            end = int(i_range[1])
            print("Range end: {}".format(end))
        except:
            parser.exit(status=1, message=error_msg['range'].format(i_range[1]))
        if end - start + 1 < 0:
            parser.exit(1, error_msg['range'].format(options.i_range))
        #print(["{}\n".format(s) for s in range(start, end + 1)])
        try:
            if echo:
                raise
        except:
          parser.exit(status=1, message=error_msg['combo'].format('-e', '-i')+def_msg)
        try:
            if len(filename) != 0:
                raise
        except:
            parser.exit(1, error_msg['extra'].format(filename)+def_msg)
  
    n_flag = options.count
    if n_flag == False:
        parser.exit(status=1, message=error_msg['no_arg'].format('n'))
    if n_flag != None:
        try:    
            count = int(options.count)
            if count < 0:
                raise 
        except:
            parser.exit(status=1, message=error_msg['line_count'].format(options.count))
    if len(args) != 0:
        if args[0][0:2] == '--':
            parser.exit(status=1, message=error_msg['unrecog'].format(args[0])+def_msg)
        elif args[0][0] == '-':
            parser.exit(status=1, message=error_msg['invalid'].format(args[0]))
        else:
            parser.exit(1, error_msg['extra'].format(args[0]))
                        
if __name__ == "__main__":
    main()
