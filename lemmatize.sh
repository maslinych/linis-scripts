#!/bin/bash
root="$1"
shift
out="$1"
shift

echo $root
echo $out

mkdir -p "$out"

for i in $root/*.txt
do
	echo $i
    mystem -nfl -e utf-8 "$i" | gawk -f ./mystem2lemmas.awk > "$out/${i##*/}"
done
