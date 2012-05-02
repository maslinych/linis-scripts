#!/bin/gawk
# select most frequent lemma (or just first if zero frequency) from mystem output
# remove unknown word marks (?) from mystem output
BEGIN{fmax=0; FS="|";}
NF>1 {
	for (i=1;i<=NF;i++) {
		split($i, f, ":"); 
		if (f[2]>fmax) {
			fmax=f[2];lemma=f[1];
		}
	} 
	if (fmax==0) {
		split($1,t,":");
		lemma=t[1];
	}; 
	print lemma; 
	fmax=0;
	next;
} 
/\?/ { 
	gsub("?", ""); 
} 
{
	split($1,l,":"); 
	print l[1];
}
