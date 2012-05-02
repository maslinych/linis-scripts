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
	echo "$i"
	hxunent "$i" | \
	sed -e :a -e 's/<img[^>]*>/ IMG /gi;/</N;//ba' | \
	sed -e :a -e 's/<a href[^>]*>/ HREF /gi;/</N;//ba' | \
	sed -e :a -e 's/<lj user="\([^"]*\)"[^>]*>/ LJUSER\1 /gi;/</N;//ba' | \
	sed -e :a -e 's/<lj-\([^ ]*\) [^>]*>/ LJ\1 /gi;/</N;//ba' | \
	sed -e 's/[:;]-\?)\+/ SMILEA /g' -e 's/))\+/ SMILEAA /g' -e 's/:-\?(\+/ SMILEU /g' -e 's/((\+/ SMILEUU /g' | \
	sed -e 's/&nbsp;/ /g' -e 's/&e[nm]dash;/ — /g' -e 's/&[lr]aquo;/"/g' | \
	sed -e :a -e 's/<[^>]*>//g;/</N;//ba' > "$out/${i##*/}"
done
