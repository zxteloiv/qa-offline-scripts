#!/binbash

# group by k, v

python attr_extractor.py ../filelist.tmp "kv"  > ../out.tmp
cat ../out.tmp | awk -F "\t" '{k=$1"\t"$3; freq[k]+=1; prop[k]=$2;}END{for (k in freq) {print freq[k]"\t"k"\t"prop[k]}}' | sort -k2,2 -k1,1gr > ../out.domain-prop-value.stat

# group by keys per example

python attr_extractor.py ../filelist.tmp "kpe"  > ../out.tmp
cat ../out.tmp | sort | uniq -c | sort -k2,2 -k1,1gr > ../out.domain-prop.per-q.stat

# group by values per example

python attr_extractor.py ../filelist.tmp "vpe"  > ../out.tmp
cat ../out.tmp | sort | uniq -c | sort -k2,2 -k1,1gr > ../out.domain-value.per-q.stat

# print sample questions by key

python attr_extractor.py ../filelist.tmp "skpe"  > ../out.tmp
cat ../out.tmp | sort -k1,1 > ../out.domain-prop.per-q.question


rm ../out.tmp

