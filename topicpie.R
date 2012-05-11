#!/usr/bin/R
topicpie <- function (word,topicinfo,ttd,threshold) {
    topics<-sort(ttd[word,][ttd[word,]>threshold])
    lbls<-topicinfo[names(topics),"label"]
    pie(topics, labels=lbls)
}
