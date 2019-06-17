#!/bin/sh

cmds=`cat /dev/stdin`

#for cmd in "$cmds"; do
    ldd `which $cmds`
#done
