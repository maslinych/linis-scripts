#!/usr/local/bin/xmlgawk -f
XMLCHARDATA { if ( XMLPATH ~ /comment\/author/ ) 
    { print $0 }
}
