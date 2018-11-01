#!/usr/bin/env bash

KIND=$1
if [ -z $KIND ] ; then
    echo "Usage: $1 [minor,major]" >&2
    exit 1
fi

# Usage: increment_version <version> [<position>]
increment_version() {
   local v=$1
   if [ -z $2 ]
   then
       local rgx='^((?:[0-9]+\.)*)([0-9]+)($)'
   else
       local rgx='^((?:[0-9]+\.){'$(($2-1))'})([0-9]+)(\.|$)'
       for (( p=`grep -o "\."<<<".$v"|wc -l`; p<$2; p++)); do
           v+=.0;
       done
   fi
   val=`echo -e "$v" | perl -pe 's/^.*'$rgx'.*$/$2/'`
   echo "$v" | perl -pe s/$rgx.*$'/${1}'`printf %0${#val}s $(($val+1))`/
}

# EXAMPLE   ------------->   # RESULT
increment_version 1          # 2
increment_version 1.0.0      # 1.0.1
increment_version 1 2        # 1.1
increment_version 1.1.1 2    # 1.2
increment_version 00.00.001  # 00.00.002



echo $VERSION > VERSION.txt
git add VERSION.txt
git commit -m "Release $VERSION"
git tag $VERSION
git push
git push --tags
