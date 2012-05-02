#!/usr/local/bin/xmlgawk -f
#BEGIN {
#    while ((getline commentor < ARGV[1]) > 0) {
#        commentors[commentor]++ }
#    }
#@load xml
XMLSTARTELEM == "post" {depth = 0}
XMLSTARTELEM == "comments" { depth++ }
XMLENDELEM == "comments" { depth-- } 
XMLCHARDATA { 
    if ( XMLPATH ~ /comment\/author/ )  {
        net[depth] = $0
        if (depth>1) {
            print net[depth-1], net[depth]}
    }  
}
