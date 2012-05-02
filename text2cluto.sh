#!/bin/bash
indir=$1
shift
outfile=$1
shift

for i in "$indir"/*.txt 
do
    echo "${i##*/},\"$(cat $i | tr "^M\n\"" " " )\""
done | iconv -c -t cp1251 > "$outfile"
