# coding: utf-8

import re, sys

def codec(fobj, encoding='utf-8'):
    for l in fobj:
        yield l.decode(encoding)

def kbfile_reader(fobj):
    example = {}
    for line in fobj:
        line = line.rstrip()
        if re.match(u'原始Q', line):
            example['q'] = line.split(u':')[1]
        elif re.match(u'原始A', line):
            example['a'] = line.split(u':')[1]
        elif re.match(u'标注Q', line):
            kvpat = r'\[([^\]]*)\]\(([^\)]*)\)'
            prop = [(k, v) for v, k in re.findall(kvpat, line)]
            example['lq'] = prop
        elif re.match(u'标注A', line):
            kvpat = r'\[([^\]]*)\]\(([^\)]*)\)'
            prop = [(k, v) for v, k in re.findall(kvpat, line)]
            example['la'] = prop
        else:
            pass

        if len(example) == 4:
            yield example

def main():

    for f in open(sys.argv[1]):
        m = re.search(r'景点|酒店|餐饮', f)
        if not m: continue
        t, f = m.group(0), f.rstrip()

        print "new file:", f
        for example in kbfile_reader(codec(open(f))):
            keys, vals = zip(*example['lq'])
            print t, u','.join(set(keys)).encode('utf-8')

    pass

if __name__ == "__main__":
    main()
            

