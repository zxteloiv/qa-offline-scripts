# coding: utf-8

import sys
import itertools
import json
import cPickle
import datetime
import copy
import re

def print_msg(msg):
    print str(datetime.datetime.now()) + "\t" + msg

def ent_cat_generator(filename):
    for line in open(filename, 'rb'):
        parts = line.decode('utf-8').rstrip().split('\t')
        yield (parts[0] if len(parts) > 0 else None, parts[1:] if len(parts) > 1 else [])

def link_generator(filename):
    for line in open(filename, 'rb'):
        line = line.decode('utf-8').rstrip().split('\t')
        if len(line) == 2:
            yield line[0], line[1]

def build_link_dict(filename):
    return dict(link_generator(filename))

def normalized_entity_name(name):
    name = name.lower()
    return name

class EntityBaseBuilder(object):
    def __init__(self):
        self.id_gen = itertools.count(1)
        self.rev_ent_index = {"en":{}, "zh":{}, "ja":{}}
        self.ent_index = {}

    def update_rev_index(self, lang, name, ent_id):
        norm_name = normalized_entity_name(name)
        self.rev_ent_index[lang][norm_name] = ent_id

    def get_rev_index(self, lang, name):
        norm_name = normalized_entity_name(name)
        return self.rev_ent_index[lang].get(norm_name)

    def add_entities_from_cat(self, f_cat, lang):
        for ent_name, _ in ent_cat_generator(f_cat):
            if not self.get_rev_index(lang, ent_name):
                # new entity encountered
                ent_id = self.id_gen.next()
                self.update_rev_index(lang, ent_name, ent_id)
                ent = {"en":"", "ja": "", "zh": "", "categories":set()}
                ent[lang] = ent_name
                self.ent_index[ent_id] = ent

    def add_categories_from_file(self, f_cat, lang):
        for ent_name, cats in ent_cat_generator(f_cat):
            ent_id = self.get_rev_index(lang, ent_name)
            if not ent_id: continue
            self.ent_index[ent_id]["categories"].update(cats)

    def expand_categories_from_dict(self, cat_link_dict):
        for ent_id in self.ent_index.iterkeys():
            new_cats = copy.copy(self.ent_index[ent_id]["categories"])
            for cat in self.ent_index[ent_id]["categories"]:
                linked_cat = cat_link_dict.get(cat)
                if linked_cat:
                    new_cats.add(linked_cat)
            self.ent_index[ent_id]["categories"] = new_cats

    def add_entities_from_bilingual_link(self, f_ent_link, lang_src, lang_to):
        for ent_src, ent_to in link_generator(f_ent_link):
            if self.get_rev_index(lang_src, ent_src):
                ent_id = self.get_rev_index(lang_src, ent_src)
                self.update_rev_index(lang_to, ent_to, ent_id)
            elif self.get_rev_index(lang_to, ent_to):
                ent_id = self.get_rev_index(lang_to, ent_to)
                self.update_rev_index(lang_src, ent_src, ent_id)
            else:
                # new entity encountered
                ent_id = self.id_gen.next()
                ent = {"en":"", "ja": "", "zh": "", "categories":set()}
                self.ent_index[ent_id] = ent
                self.update_rev_index(lang_src, ent_src, ent_id)
                self.update_rev_index(lang_to, ent_to, ent_id)

            self.ent_index[ent_id][lang_to] = ent_to
            self.ent_index[ent_id][lang_src] = ent_src

    def export_ent_to_file(self, filename):
        with open(filename, "wb") as f:
            for k, v in self.ent_index.iteritems():
                v["id"] = k
                v["categories"] = list(v["categories"])
                out = str(k) + '\t' + json.dumps(v)
                f.write(out + '\n')
                f.flush()

    def save_state(self, ent_index_file, rev_ent_index_file):
        cPickle.dump(self.ent_index, ent_index_file)
        cPickle.dump(self.rev_ent_index, rev_ent_index_file)

    def load_state(self, ent_index_file, rev_ent_index_file):
        self.ent_index = cPickle.load(ent_index_file)
        self.rev_ent_index = cPickle.load(rev_ent_index_file)
        self.id_gen = itertools.count(len(self.ent_index) + 1)

def build_entity_base():
    # build entity base
    f_ent_cate_en = 'entity-category-en.txt.refinement'
    f_ent_cate_zh = 'entity-category-zh.txt.refinement'
    f_ent_cate_ja = 'entity-category-ja.txt.refinement'
    f_ent_en_ja = 'lang-ent-links-en-ja.txt'
    f_ent_en_zh = 'lang-ent-links-en-zh.txt'
    f_ent_ja_en = 'lang-ent-links-ja-en.txt'
    f_ent_ja_zh = 'lang-ent-links-ja-zh.txt'
    f_ent_zh_en = 'lang-ent-links-zh-en.txt'
    f_ent_zh_ja = 'lang-ent-links-zh-ja.txt'

    entity_base = EntityBaseBuilder()
    # add English entities first, then its closure
    print_msg("import en cat file...")
    entity_base.add_entities_from_cat(f_ent_cate_en, "en")
    print_msg("import en-ja link file...")
    entity_base.add_entities_from_bilingual_link(f_ent_en_ja, "en", "ja")
    print_msg("import en-zh link file...")
    entity_base.add_entities_from_bilingual_link(f_ent_en_zh, "en", "zh")
    print_msg("import ja-en link file...")
    entity_base.add_entities_from_bilingual_link(f_ent_ja_en, "ja", "en")
    print_msg("import ja-zh link file...")
    entity_base.add_entities_from_bilingual_link(f_ent_ja_zh, "ja", "zh")
    print_msg("import zh-en link file...")
    entity_base.add_entities_from_bilingual_link(f_ent_zh_en, "zh", "en")
    print_msg("import zh-ja link file...")
    entity_base.add_entities_from_bilingual_link(f_ent_zh_ja, "zh", "ja")

    # add entities in other languages
    print_msg("import zh cat file...")
    entity_base.add_entities_from_cat(f_ent_cate_zh, "zh")
    print_msg("import ja cat file...")
    entity_base.add_entities_from_cat(f_ent_cate_ja, "ja")

    return entity_base

def add_categories(entity_base):
    # add categories to the entity
    f_ent_cate_en = 'entity-category-en.txt.refinement'
    f_ent_cate_zh = 'entity-category-zh.txt.refinement'
    f_ent_cate_ja = 'entity-category-ja.txt.refinement'
    f_cate_en_ja = 'lang-cate-links-en-ja.txt'
    f_cate_en_zh = 'lang-cate-links-en-zh.txt'
    f_cate_ja_en = 'lang-cate-links-ja-en.txt'
    f_cate_ja_zh = 'lang-cate-links-ja-zh.txt'
    f_cate_zh_en = 'lang-cate-links-zh-en.txt'
    f_cate_zh_ja = 'lang-cate-links-zh-ja.txt'
    print_msg("build cate link en to ja...")
    cat_link_en_ja = build_link_dict(f_cate_en_ja)
    print_msg("build cate link en to zh...")
    cat_link_en_zh = build_link_dict(f_cate_en_zh)
    print_msg("build cate link zh to ja...")
    cat_link_zh_ja = build_link_dict(f_cate_zh_ja)
    print_msg("build cate link zh to en...")
    cat_link_zh_en = build_link_dict(f_cate_zh_en)
    print_msg("build cate link ja to en...")
    cat_link_ja_en = build_link_dict(f_cate_ja_en)
    print_msg("build cate link ja to zh...")
    cat_link_ja_zh = build_link_dict(f_cate_ja_zh)
    print_msg("add cate from file %s..." % f_ent_cate_en)
    entity_base.add_categories_from_file(f_ent_cate_en, "en")
    print_msg("add cate from file %s..." % f_ent_cate_zh)
    entity_base.add_categories_from_file(f_ent_cate_zh, "zh")
    print_msg("add cate from file %s..." % f_ent_cate_ja)
    entity_base.add_categories_from_file(f_ent_cate_ja, "ja")
    print_msg("expand cate using link %s..." % f_cate_en_ja)
    entity_base.expand_categories_from_dict(cat_link_en_ja)
    print_msg("expand cate using link %s..." % f_cate_en_zh)
    entity_base.expand_categories_from_dict(cat_link_en_zh)
    print_msg("expand cate using link %s..." % f_cate_zh_en)
    entity_base.expand_categories_from_dict(cat_link_zh_en)
    print_msg("expand cate using link %s..." % f_cate_zh_ja)
    entity_base.expand_categories_from_dict(cat_link_zh_ja)
    print_msg("expand cate using link %s..." % f_cate_ja_en)
    entity_base.expand_categories_from_dict(cat_link_ja_en)
    print_msg("expand cate using link %s..." % f_cate_ja_zh)
    entity_base.expand_categories_from_dict(cat_link_ja_zh)

    return entity_base

def main():
    entity_base = build_entity_base()
    entity_base = add_categories(entity_base)

    # output to see
    output_file = sys.argv[1]
    print_msg("export to %s..." % output_file)
    entity_base.export_ent_to_file(output_file)

def test():
    entity_base = EntityBaseBuilder()
    entity_base.add_entities_from_cat("test_en", "en")
    entity_base.add_entities_from_bilingual_link("test_en_zh", "en", "zh")
    entity_base.add_entities_from_cat("test_zh", "zh")
    entity_base.add_categories_from_file("test_en", "en")
    entity_base.add_categories_from_file("test_zh", "zh")

    entity_base.export_ent_to_file("output")

if __name__ == "__main__":
    main()


