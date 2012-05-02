#!/usr/local/bin/xmlgawk -f
# reads xml blog export and creates txt file for each comment
XMLCHARDATA { 
    switch ( XMLPATH ) {
        case /comment\/author/: 
            if ( $0 == "" ) { 
                ncomment["anonymous"]++
                author = "anonymous" ncomment["anonymous"]
            }
            else
                { author = $0 }
            ncomment[author]++
            commentid = author "." ncomment[author]
            break

        case /comment\/text/:
            gsub("\n", " ") 
            gsub(/"/, "\"\"")
            commenttext = $0
            printf "%s,%s,\"%s\"\n",  post, commentid, commenttext
            break

        case /url/:
            post = $0
            break
    }
}
XMLENDELEM == "comment" {
    if (! commentid in alwaysprinted) {
    printf "%s,%s,\"%s\"\n",  post, commentid, commenttext
    alwaysprinted[commentid] = 1
    }
}
