#!/bin/bash

COUNTRY=$1
ROOT=$2;

if [ "$1" == "cn" ]; then
    echo "==========景点===========";

    find $ROOT -name "景点*.json" | xargs cat | jq 'keys' | awk -F '"' '{arr[$2]+=1}END{for(k in arr) {print k"\t"arr[k]}}' | sort -k2,2g;

    echo "==========餐厅===========";

    find $ROOT -name "餐厅*.json" | xargs cat | jq 'keys' | awk -F '"' '{arr[$2]+=1}END{for(k in arr) {print k"\t"arr[k]}}' | sort -k2,2g;

    echo "==========酒店===========";

    find $ROOT -name "酒店*.json" | xargs cat | jq 'keys' | awk -F '"' '{arr[$2]+=1}END{for(k in arr) {print k"\t"arr[k]}}' | sort -k2,2g;

elif [ "$1" == "jp" ]; then

    echo "==========餐厅===========";
    find $ROOT -name "*.json" | xargs cat | jq 'keys' | awk -F '"' '{arr[$2]+=1}END{for(k in arr) {print k"\t"arr[k]}}' | sort -k2,2g;

fi


