
# select count(1) from all group by city, domain

echo "北京	餐饮	"$(cat ../filelist.tmp | grep '.*客观北京.*餐饮.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "上海	餐饮	"$(cat ../filelist.tmp | grep '.*客观上海.*餐饮.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "广州	餐饮	"$(cat ../filelist.tmp | grep '.*客观广州.*餐饮.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "日本	餐饮	"$(cat ../filelist.tmp | grep '.*客观日本.*餐饮.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)

echo "北京	酒店	"$(cat ../filelist.tmp | grep '.*客观北京.*酒店.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "上海	酒店	"$(cat ../filelist.tmp | grep '.*客观上海.*酒店.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "广州	酒店	"$(cat ../filelist.tmp | grep '.*客观广州.*酒店.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "日本	酒店	"$(cat ../filelist.tmp | grep '.*客观日本.*酒店.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)

echo "北京	景点	"$(cat ../filelist.tmp | grep '.*客观北京.*景点.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "上海	景点	"$(cat ../filelist.tmp | grep '.*客观上海.*景点.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "广州	景点	"$(cat ../filelist.tmp | grep '.*客观广州.*景点.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
echo "日本	景点	"$(cat ../filelist.tmp | grep '.*客观日本.*景点.*.txt'  | xargs grep -P '^标注Q:' | wc -l | tail -1)
