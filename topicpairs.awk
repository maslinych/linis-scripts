#!/bin/gawk -f
BEGIN { FS=","; }
{ l[NR] = $0 ; w[$2]++ ; w[$3]++ }
END { for (i in l) { 
    split(l[i], a, ",")
    if ((w[a[2]] == 1) && (w[a[3]] == 1)) { print l[i]} 
    }
}

