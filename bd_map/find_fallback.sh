#!/bin/bash

# find the uid that failed to crawl and fallback to the homepage of BaiduMap.

DIR=$1

grep -P '^<title>' $DIR -m 1 -R | grep -P '百度地图' | awk -F"/|:" '{print $3"/"$4}'


