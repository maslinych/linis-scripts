#!/bin/bash

txtdir="$1"
shift
out="$1"
shift

#metadata="$txtdir/metadata.csv"
#test -f "$metadata" || { echo "No metadata.csv file"; exit 1 }
#numtexts=$(cat "$metadata" | wc -l)
#test $(($(ls "$txtdir/*.txt" | wc -l)-1)) -eq $numtexts || { echo "Number of texts doesn't match metadata.csv file" ; exit 1 }

tempfile="$(mktemp)"
trap 'rm -f "$tempfile"' EXIT

pushd "$txtdir"
for t in *.txt
do
    echo "${t%%.txt},$(cat "$t" | hxunent | tr '\n' ' ')" >> "$tempfile"
done 
popd

sort -n "$tempfile" > "$out"

#test $(cat "$tempfile" | wc -l) -eq $numtexts || { echo "CSV lines number check failed"; exit 1 }

#join -t, -j1 "$metadata" "$tempfile" > "$out" 
