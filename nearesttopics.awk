#!/bin/gawk -f 
BEGIN { FS=","; }
($2 in a) && ($3 in b)  { next }
{a[$2] = $1 ; b[$3] = $1 ; print }
