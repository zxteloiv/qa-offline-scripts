# coding: utf-8

import sys, re

def cleanup(word):
    word = re.sub('\[\[.*\|(.*)\]\]', r'\1', word) # replace the link with the anchor text: [[something|anchor]] -> anchor
    word = re.sub('\[\[([^\|]*)\|?$', r'\1', word) # left part of a link: [[something -> something
    word = re.sub('\[\[[^\|]*\|([^\]]*)$', r'\1', word) # left and right part of a link: [[something|anchor -> anchor
    word = re.sub('[^\|]*\|(.*)\]\]', r'\1', word) # right part of a link: something|anchor]] -> anchor
    word = re.sub('.*\|(.*)$', r'\1', word) # middle part of a link: something|anchor -> anchor
    word = re.sub('[\[\]\|]', '', word) # remove all [, ] and |
    return word

def cleanup_predicate_match(filename):
    for line in open(filename):
        parts = line.rstrip().split('\t')
        try:
            src, dest, score = cleanup(parts[0]), cleanup(parts[1]), parts[2]
        except:
            continue

        print "\t".join((src, dest, score))

if __name__ == "__main__":
    cleanup_predicate_match(sys.argv[1])








