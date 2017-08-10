# coding: utf-8

import re, sys, os.path
import json

def codec(fobj, encoding='utf-8'):
    for l in fobj:
        yield l.decode(encoding)

def kbfile_reader(fobj):
    example = {}
    for i, line in enumerate(fobj):
        line = line.rstrip()
        if re.match(u'原始Q', line):
            if 'q' in example:
                raise ValueError("Parsing Error: question existed at line:%d" % i)
            example['q'] = re.split(u':|：', line)[1]
        elif re.match(u'原始A', line):
            if 'a' in example:
                raise ValueError("Parsing Error: answer existed at line:%d" % i)
            example['a'] = re.split(u':|：', line)[1]
        elif re.match(u'标注Q', line):
            kvpat = r'\[([^\]]*)\]\(([^\)]*)\)'
            prop = sorted([(k.strip(), v.strip()) for v, k in re.findall(kvpat, line)])
            if 'lq' in example:
                raise ValueError("Parsing Error: question label existed at line:%d" % i)
            example['lq'] = prop
        elif re.match(u'标注A', line):
            kvpat = r'\[([^\]]*)\]\(([^\)]*)\)'
            prop = sorted([(k.strip(), v.strip()) for v, k in re.findall(kvpat, line)])
            if 'la' in example:
                raise ValueError("Parsing Error: answer label existed at line:%d" % i)
            example['la'] = prop
        else:
            pass

        if len(example) == 4:
            yield example
            example = {}

def main():

    req = sys.argv[2]
    if req == 'skpe':
        question_printer = get_question_printer_by_keys_per_example()

    for f in open(sys.argv[1]):
        m = re.search(r'景点|酒店|餐饮', os.path.basename(f))
        if not m: continue
        t, f = m.group(0), f.rstrip()


        for example in kbfile_reader(codec(open(f))):
            if req == 'kv':
                print_qlabel_kv(example, t)
            elif req == 'vpe':
                print_qlabel_values_per_example(example, t)
            elif req == 'kpe':
                print_qlabel_keys_per_example(example,t)
            elif req == 'skpe':
                question_printer(example, t)

    pass

def print_qlabel_kv(example, t):
    if 'lq' not in example or not example['lq']: return
    for k, v in example['lq']:
        print '\t'.join((t, k.encode('utf-8'), v.encode('utf-8')))

def print_qlabel_values_per_example(example, t):
    if 'lq' not in example or not example['lq']: return
    keys, vals = zip(*example['lq'])
    value = u','.join(v for k, v in example['lq'] if k not in (u'实体', u'地点'))
    print t + '\t' + value.encode('utf-8') + '\t' + u','.join(sorted(set(keys))).encode('utf-8')

def print_qlabel_keys_per_example(example, t):
    if 'lq' not in example or not example['lq']: return
    keys, vals = zip(*example['lq'])
    print t + '\t' + u','.join(sorted(set(keys))).encode('utf-8')

def get_question_printer_by_keys_per_example():
    questions = {}
    def printer(example, t):
        if 'lq' not in example or not example['lq']: return
        keys, vals = zip(*example['lq'])
        keys = u','.join(sorted(set(keys)))
        if keys not in questions:
            questions[keys] = example['q']
            print t + '\t' + keys.encode('utf-8') + '\t' + example['q'].encode('utf-8')
    return printer

if __name__ == "__main__":
    main()


