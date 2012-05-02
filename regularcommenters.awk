#!/usr/local/bin/xmlgawk -f
BEGIN {post=0}
XMLSTARTELEM ~ "post" { 
    #print post
    post++
    delete lastpost
}
XMLCHARDATA { 
    if ( XMLPATH ~ /comment\/author/ ) {
        if  (! lastpost[$0] == 1 ) {
        commenters[$0]++
        #print $0, commenters[$0]
        lastpost[$0] = 1
        }
    }
}
END { 
    print "#total posts:", post
    cutoff = 1
    for (c in commenters) {
        #if (commenters[c] > cutoff) {
        #print sqrt(commenters[c]/post), c
        print commenters[c], c
    #}
    }
} 
