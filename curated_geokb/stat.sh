#!/binbash

python attr_extractor.py ../filelist.tmp  > ../out.tmp
cat ../out.tmp | awk -F "\t" '{k=$1"\t"$3; freq[k]+=1; prop[k]=$2;}END{for (k in freq) {print freq[k]"\t"k"\t"prop[k]}}' | sort -k2,2 -k1,1gr > ../out.domain-value.stat
