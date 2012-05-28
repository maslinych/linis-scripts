#!/usr/bin/R
library(reshape)
topicdiff <- function(dtd) {
    # format of DTD table: colnames = month, id, author, topics...
    # dtdm<-melt(dtd, id=c('month','author','id'))
    # dtdam <- cast(dtdm, author + month ~ variable , sum)
    topicnames <- colnames(dtd[,4:ncol(dtd)])
    dtdam <- cast(melt(dtd, id=c('month','author','id'), measure.vars=topicnames), author + month ~ variable, sum)
    dtdam2 <- subset(dtdam,count(dtdam, "author")$freq==2)
    # dtdamm2<-melt.data.frame(dtdam2,id=c('author','month'),measure.vars=c(colnames(dtdam2[,3:])))
    # dtddiff2<-cast(dtdamm2, author ~ variable,diff)
    return(cast(melt.data.frame(dtdam2,id=c('author','month'),measure.vars=topicnames), author ~ variable, diff))
}
