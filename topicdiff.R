#!/usr/bin/R
library(reshape)
topicmelt <- function(dtd) {
    # format of DTD table: colnames = month, id, author, topics...
    # dtdm<-melt(dtd, id=c('month','author','id'))
    # dtdam <- cast(dtdm, author + month ~ variable , sum)
    topicnames <- colnames(dtd[,4:ncol(dtd)])
    dtdam <- cast(melt(dtd, id=c('month','author','id'), measure.vars=topicnames), author + month ~ variable, sum)
    return(subset(dtdam,count(dtdam, "author")$freq==2))
    # dtdamm2<-melt.data.frame(dtdam2,id=c('author','month'),measure.vars=c(colnames(dtdam2[,3:])))
    # dtddiff2<-cast(dtdamm2, author ~ variable,diff)
    #return(cast(melt.data.frame(dtdam2,id=c('author','month'),measure.vars=topicnames), author ~ variable, diff))
}

topicposts <- function(dtd,topics) {
    # politpostm <- melt(dtd,id=c('month','id','author'),measure.vars=topics)
    # politpost<-cast(politpostm, author + month + id ~ ., sum)
    # colnames(politpost) <- c('author','month','id','polit')
    # aggregation by MEAN VALUE
    # politauthors<-aggregate(polit ~ author + month,politpost,mean)
    # politdiff<-cast(melt(politauthors, id=c('author', 'month'), measure.vars=c('polit')), author ~ ...)
    # politdiff2<-na.omit(politdiff)
    # politdiff2<-cbind(politdiff2, politdiff2$"12_polit" - politdiff2$"9_polit")

    # politpostm <- melt.data.frame(dtdam,id=c('month','author'),measure.vars=polittopics)
    # politpost<-cast(politpostm, author + month ~ ., sum)
    # 
    cast(melt.data.frame(dtdam, id=c('author','month'), measure.vars=polittopics),author + month ~ ., sum)
    return()
}

topicprops <- function(dtd) {
    # summarize topic values by author/month
    dtdam <- cast(melt(dtd, id=c('month','author','id'), measure.vars=topicnames), author + month ~ variable, sum)
    # 
    # get proportion of each topic in all author's posts:
    #   divide topic values by row sum (number of posts)
    #   multiply by 100 to get percents
    dtdam[,3:ncol(dtdam)]<-as.matrix((dtdam[,3:ncol(dtdam)])/rowSums(dtdam[,3:ncol(dtdam)])*100)
    return(dtdam)
}
