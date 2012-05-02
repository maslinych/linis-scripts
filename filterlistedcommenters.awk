#!/bin/gawk -f
BEGIN {
    while ((getline author < ARGV[1]) > 0) {
        authors[author] = 1}
}
{ for (i=1;i<=2;i++) {
    if (authors[$i] != 1) {next;}}}
{print}
