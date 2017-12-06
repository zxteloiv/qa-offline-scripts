# coding: utf-8

import os, sys

def make_basename(domain, prop):
    domain_map = {
            u'餐饮': u'catering',
            u'酒店': u'hotel',
            u'景点': u'tour',
            u'cater': u'catering',
            u'hotel': u'hotel'
            }

    if domain not in domain_map:
        return None

    prop_map = {
            u"地点": u"location",
            u"实体": u"entity",
            u"地址": u"address",
            u"门票价格": u"price",
            u"领域": u"category",
            u"电话": u"phone",
            u"营业时间": u"opening_hour",
            u"每晚最低价格": u"price_per_night",
            u"酒店服务": u"service",
            u"酒店设施": u"hotel_facility",
            u"房间设施": u"room_facility",
            u"入离店时间": u"check-in_time",
            u"人均消费": u"price",
            u"推荐菜品": u"dish"
            }

    if prop not in prop_map:
        return None

    basename = u"_".join((domain_map[domain], prop_map[prop]))
    return basename.encode('utf-8') + '.txt'

def codec(fobj, encoding='utf-8'):
    for l in fobj:
        yield l.decode(encoding)

def main():
    dirpath = sys.argv[2] if len(sys.argv) > 2 else '.'
    for line in codec(open(sys.argv[1])):
        p = line.rstrip().split('\t')
        basename = make_basename(p[0], p[1])
        if not basename:
            raise ValueError("basename not available: %s" % line.rstrip().encode('utf-8'))

        filepath = os.path.join(dirpath, basename)
        with open(filepath, 'a') as f:
            f.write(p[2].encode('utf-8') + '\t' + str(p[3]) + '\n')
            f.close()


if __name__ == "__main__":
    main()


