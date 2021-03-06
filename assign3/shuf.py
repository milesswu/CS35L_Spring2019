#!/usr/bin/python

import random, sys
import argparse

#Global msgs
prog_name=argparse._sys.argv[0]
def_msg= """Try '{} --help' for more information.\n""".format(prog_name)
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
    'no_repeat': prog_name + ": no lines to repeat\n",
    'mult_opt': prog_name + ": multiple {} options specified\n"
}

#Exception Classes for all instances of error handling
class Error(Exception):
    pass

class ExtraOperands(Error):
    def __init__(self, operand):
        self.err = error_msg['extra'].format(operand)+def_msg
class InvalidOption(Error):
    def __init__(self, option):
        self.err = error_msg['invalid'].format(option)+def_msg
class UnrecogOption(Error):
    def __init__(self, option):
        self.err = error_msg['unrecog'].format(option)+def_msg
class InvalidRange(Error):
    def __init__(self, operand):
        self.err = error_msg['range'].format(operand)
class InvalidLines(Error):
    def __init__(self, count):
        self.err = error_msg['line_count'].format(count)
class NoArgs(Error):
    def __init__(self, option):
        self.err = error_msg['no_arg'].format(option)+def_msg
class InvalidCombo(Error):
    def __init__(self, opt1, opt2):
        self.err = error_msg['combo'].format(opt1, opt2)+def_msg
class NoLines(Error):
    err = error_msg['no_repeat']
class InvalidMultOpt(Error):
    def __init__(self, option):
        self.err = error_msg['mult_opt'].format(option)

#helper function to check if i_range is valid
def handle_irange(i_flag):
    start = None
    end = None
    try:
        range_err = i_flag
        i_range = list(i_flag.split('-', 1))
        range_err = i_range[0]
        start = int(i_range[0])
        
        range_err = i_range[1]
        end = int(i_range[1])
        
        if  end - start + 1 < 0:
            range_err = i_flag
            raise
    except:
        return [ True, range_err ]
    return [ False, [ i for i in range(start, end + 1) ] ]

#helper function that parses input (with desired data types) and handles errors
def handle_errors(parser, options, args):
    filename = options.filename

    #Handle input and error calling for the --echo option
    try:
        echo = bool(options.echo)
    except:
        raise InvalidOption(options.echo)

    #Handle input and error calling for the --input-range option
    i_flag = options.i_range
    list_range = None
    if i_flag == False:
        raise NoArgs('i')
    elif i_flag != None:
        if len(i_flag) > 1:
            raise InvalidMultOpt('i')
        i_error = handle_irange(i_flag[0])
        if i_error[0] == True:
            raise InvalidRange(i_error[1])
        else:
            list_range = i_error[1]
        if echo:
            raise InvalidCombo('-e', '-i')
        if len(filename) != 0:
            raise ExtraOperands(filename)

    #Handle input and error calling for the --head-count option
    n_flag = options.count
    count = None
    if n_flag == False:
        raise NoArgs('n')
        #parser.exit(1, error_msg['no_arg'].format('n'))
    if n_flag != None:
        try:    
            count = int(options.count)
            if count < 0:
                raise 
        except:
            raise InvalidLines(options.count)

    #Handle input and error calling for the --repeat option
    try:
        repeat = bool(options.repeat)
    except:
        raise InvalidOption(options.repeat)
        
    if len(args) != 0:
        if args[0][0:2] == '--':
            raise UnrecogOption(args[0])
        elif args[0][0] == '-' and len(args[0]) > 1:
            raise InvalidOption(args[0])
        elif echo:
            pass
        else:
            raise ExtraOperands(args[0])

    return {
        'file': filename,
        'e': echo,
        'i': i_flag,
        'range': list_range,
        'count': count,
        'r': repeat  
            }

#Class that is created in main and has its shuffle function called
#Performs the shuf functionality
class shuf:
    def __init__(self, args, filename, echo, i_flag, i_range, count, repeat):
        self.repeat = repeat
        self.input_text = ''

        #Set input_text based on option inputs
        if i_flag != None:
            self.input_text = [ '{}\n'.format(i) for i in i_range ]
        elif echo:
            arglist = [ s + '\n' for s in args ]
            filelist = []
            if filename != '':
                filelist = [ filename + '\n' ]
            self.input_text = filelist + arglist #handle shuf -- shuf -e -- etc
        elif len(filename) == 0 or filename == '-':
            self.input_text = sys.stdin.readlines()
        else:
            f = open(filename)
            self.input_text = f.readlines()
            f.close()

        #correct count if necesary
        self.count = count
        if count > len(self.input_text) and not repeat:
            self.count = len(self.input_text)
        #create a random ordering of input_text's lines
        self.lines = list(range(len(self.input_text)))
        random.shuffle(self.lines)
        
    def shuffle(self):
        if self.repeat:
            if not self.input_text:
                raise NoLines
            i = 0
            while i < self.count:
                sys.stdout.write(random.choice(self.input_text))
                i = i + 1
        else:
            i = 0
            while i < self.count:
                sys.stdout.write(self.input_text[self.lines[i]])
                i = i + 1
                
def main():    
    usage_msg="""Usage: {} [OPTION]... [FILE]
  or:  {} -e [OPTION]... [ARG]...
  or:  {} -i LO-HI [OPTION]...
Write a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input.

Mandatory arguments to long options are mandatory for short options too.
  -e, --echo                treat each ARG as an input line
  -i, --input-range=LO-HI   treat each number LO through HI as an input line
  -n, --head-count=COUNT    output at most COUNT lines
  -r, --repeat              output lines can be repeated
      --help     display this help and exit
""".format(prog_name, prog_name, prog_name)

    #create parser
    parser = argparse.ArgumentParser(prog='shuf.py', add_help=False, usage=def_msg) 
    #add arguments (name/flag, [action], [nargs], [const], [default]
    parser.add_argument("--help", action="store_true", dest="show_help", default=False) 
    parser.add_argument("-e", "--echo", action="store_true", dest="echo", default=False)
    parser.add_argument('-i', '--input-range', action="append", dest="i_range", nargs='?', const=False)
    parser.add_argument('-n', '--head-count', action="store", dest="count", default=sys.maxsize,
                        nargs='?', const=False)
    parser.add_argument('-r', '--repeat', action="store_true", dest="repeat", default=False)
    parser.add_argument('filename', action="store", nargs='?', const=False, default='')
    options, args = parser.parse_known_args()

    #Handle help cmd
    try:
        show_help = bool(options.show_help)
    except:
        parser.exit(1, error_msg['invalid'].format(options.show_help))
    if show_help:
            print(usage_msg)
            parser.exit(0)
    #print(options, args)
    #Both parse all option inputs and perform error handling on them
    try:
        arg_results = handle_errors(parser, options, args)
    except InvalidOption as e:
        parser.exit(1, e.err)
    except UnrecogOption as e:
        parser.exit(1, e.err)
    except InvalidRange as e:
        parser.exit(1, e.err)
    except InvalidLines as e:
        parser.exit(1, e.err)
    except NoArgs as e:
        parser.exit(1, e.err)
    except InvalidCombo as e:
        parser.exit(1, e.err)
    except InvalidMultOpt as e:
        parser.exit(1, e.err)
    except ExtraOperands as e:
        parser.exit(1, e.err)
        
    #Create shuf class and call its shuffle function
    try:
        writer = shuf(args,
                      arg_results['file'],
                      arg_results['e'],
                      arg_results['i'],
                      arg_results['range'],
                      arg_results['count'],
                      arg_results['r'])
        writer.shuffle()
    except IOError as e:
        strerror = e.strerror
        parser.exit(1, 'read/write error: {}\n'.format(strerror))
    except KeyboardInterrupt:
        parser.exit(130)
    except NoLines as e:
        parser.exit(1, e.err)
        
if __name__ == "__main__":
    main()
