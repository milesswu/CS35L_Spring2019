#!/bin/sh

#functions to call when stderr output is necessary
error_exit()
{
    echo "$1" >&2
    exit 1
}

error()
{
    echo "$1" >&2
}

#checks that given name follows guidelines
isValidName() {
    local name=$1
    case "${name:0:1}" in
    '.')
       if [ "$name" != "." ] && [ "$name" != ".." ]
       then
	   return 0 
       fi
       ;;
    '-')
	return 0
	;;
    esac
    
    if [ "${#name}" -gt 14 ] 
    then
	return 0
    fi
    if [ `echo $name | grep -E ^[A-Za-z._\-]+$ | wc -l` == 1 ]
    then
	return 1
    else
	return 0
    fi
}

#corrects/checks operand directory name
handle_dir_name()
{
    if [ "$dir" == '' ]
    then
	dir='.'
	return
    fi
    lastComp=''
    if [ "${dir:0:1}" == '/' ]
    then
	dir="${dir:1:${#dir}}"
    fi
    if [ "${dir:${#dir}-1:1}" == '/' ] 
    then
	dir="${dir:0:${#dir}-1}"
    fi
    lastComp=${dir##*/}
    isValidName "$lastComp"
    if [ "$?" == 0 ] || [ ! -d "$dir" ]
    then
	error_exit "Invalid initial directory name!"
    fi
}

#function that tests if ls output is same as directory path
lsTest()
{
    local dir=$1
    local lsOut=$2
    if [ "$dir" == "$lsOut" ]
    then
       return 1
    fi
    return 0;
}

#function that looks for duplicates of path names (case insensitive)
hasDuplicates()
{
    local dir=$1
    local file=$2
    if [ `ls -A -1 $dir | grep -i "^$file$" | wc -l` == 1 ]
    then
        return 0
    else
	return 1
    fi
}

#function to check permissions. Return 1 if a DIRECTORY has read permissions
hasPermission()
{
    local dir=$1
    local file=$2
    if [ ! -d "$dir/$file" ]
    then
	return 1
    elif [ -r "$dir/$file" ]
    then
	return 1
    else
	return 0
    fi
}

#Recursive function that traverses through all directories/subdirectories/files
#and tests if they have valid names, if they have read permissions, and if they
#have duplicates. Prints those that violate guidelines in spec.
search_dir() {
    local curDir=$1

    #parse all paths
    local lsOut=`ls -A -1 $curDir |  sort -u`
    local numPaths=`ls -A -1 $curDir | sort -u | wc -l`

    #see if ls printed working directory path
    if [ "$numPaths" == 1 ]
    then
	lsTest "$curDir" "$lsOut"
	if [ "$?" == 1 ]
	then
	   return
	fi
    fi
  
    while [ "$numPaths" -gt 0 ]
    do
	local fileComp=`ls -A -1 $curDir | sort -u | sed -n "${numPaths}p"`
	isValidName "$fileComp"
	local valid="$?"	
	hasPermission "$curDir" "$fileComp"
	local perm="$?"
	if [ "$perm" == 0 ]
	then
	    error "No permissions for: $curDir/$fileComp"
	fi
	
	if [ "$valid" == 1 ]
	then
	    hasDuplicates "$curDir" "$fileComp"
	    local dup="$?"    
	    if [ "$perm" == 1 ] &&  [ ! -h "$curDir/$fileComp" ] &&
		   [ "$dup" == 0 ] 
	    then
		if !([ ! -f "$curDir/$fileComp" ] &&
			 [ ! -d "$curDir/$fileComp" ])
		then
		    
	        
		    search_dir "$curDir/$fileComp"
		fi
	    fi
	    if [ "$dup" == 1 ]
	    then
		echo "$curDir/$fileComp"
	    fi
	else
	    echo "$curDir/$fileComp"
	fi
	(( numPaths=numPaths-1 ))
    done
}

dir=$1
invalid=$2
if [ ! -z "$invalid" ]
then
   error_exit "Too many operands!"
fi
handle_dir_name
search_dir "$dir"
