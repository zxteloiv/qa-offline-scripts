#!/bin/bash

python dump.py > out

# duplicated results are not useful, thus uniq them

cat out | awk -F "\t" '(/^cater\t名称/) {print $3"\t"1}' | sort | uniq > catering_entity.txt
cat out | awk -F "\t" '(/^cater\t推荐菜品/) {print $3"\t"1}' | sort | uniq > catering_dish_cond.txt
cat out | awk -F "\t" '(/^hotel\t名称/) {print $3"\t"1}' | sort | uniq > hotel_entity.txt
cat out | awk -F "\t" '(/^hotel\t酒店设施/) {print $3"\t"1}' | sort | uniq > hotel_hotel_facility_cond.txt
cat out | awk -F "\t" '(/^hotel\t房间设施/) {print $3"\t"1}' | sort | uniq > hotel_room_facility_cond.txt
cat out | awk -F "\t" '(/^hotel\t酒店服务/) {print $3"\t"1}' | sort | uniq > hotel_hotel_service_cond.txt
cat out | awk -F "\t" '(/^tour\t名称/) {print $3"\t"1}' | sort | uniq > tour_entity.txt

rm out
