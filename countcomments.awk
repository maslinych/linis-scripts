#!/usr/local/bin/xmlgawk -f
#BEGIN {
#    while ((getline commentor < ARGV[1]) > 0) {
#        commentors[commentor]++ }
#    }
#@load xml
XMLENDELEM == "post" {printf "%s,%s\n", url, comments; comments = 0}
XMLSTARTELEM == "comment" { comments++ }
XMLCHARDATA { 
    if ( XMLPATH ~ /post\/url/ )  {
        url = $0
    }  
}
