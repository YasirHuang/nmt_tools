from __future__ import print_function
import json
import spacy
import argparse

from tqdm import tqdm

def conject_postag(src_sent, sent_doc):
    word_idx = 0
    conject = False
    ret_pos = []
    for token in sent_doc:
        word_from_doc = token.text
        word_from_src = src_sent[word_idx:word_idx + len(word_from_doc)]
        if word_from_doc != word_from_src:
            raise ValueError("wrong alignment!")

        if conject:
            ret_pos[-1] = '-'.join([ret_pos[-1], token.pos_])
        else:
            ret_pos.append(token.pos_)
        if word_idx + len(word_from_doc) < len(src_sent):
            if src_sent[word_idx + len(word_from_doc)] == ' ':
                word_idx += len(word_from_doc) + 1
                conject = False
            else:
                word_idx += len(word_from_doc)
                conject = True
    if not len(ret_pos) == len(src_sent.strip().split()):
        raise ValueError('wrong conject!')
    return ret_pos
def tag_sentence(nlp, src_sentence, key_word_list, key_word_pos_list):
    phrases = sorted(src_sentence['phrases'], key=lambda item: item['first_word_index'])
    sentence = src_sentence['sentence'].strip().split()

    sentence_doc = nlp(src_sentence['sentence'])
    sentence_pos = conject_postag(src_sentence['sentence'], sentence_doc)
    assert len(sentence) == len(sentence_pos)
    
    key_tag = [None] * len(sentence)
    all_tag = [None] * len(sentence)
    for phrase in phrases:
        first_word_index = phrase['first_word_index']
        phrase_len = len(phrase['phrase'].strip().split())
        for i in range(phrase_len):
            if sentence_pos[i + first_word_index] in key_word_pos_list or \
                    (key_word_list is not None and sentence[i + first_word_index] in key_word_list):
                key_tag[i + first_word_index] = phrase['phrase_id']
            all_tag[i + first_word_index] = phrase['phrase_id']
    return key_tag, all_tag

def tag_corpus(splits, sentences_json, key_word_list, key_word_pos_list):
    nlp = spacy.load('en_core_web_sm')
    for split_id in tqdm(splits):
        src_sentence_json = sentences_json[split_id]
        key_tag, all_tag = tag_sentence(nlp, src_sentence_json, key_word_list, key_word_pos_list)
        sentences_json[split_id]['all_tag'] = all_tag
        sentences_json[split_id]['key_tag'] = key_tag

def add_word_tag(splits_file, json_file, output_json_file, key_word_list_file, key_word_pos_list_file):
    
    with open(splits_file, 'r') as fp:
        splits = [s.strip().split('.')[0] for s in fp.readlines()]
    with open(json_file, 'r', encoding='utf-8') as fp:
        sentences_json = json.load(fp)
    with open(key_word_pos_list_file, 'r') as fp:
        key_word_pos_list = [l.strip() for l in fp.readlines()]
    if key_word_list_file is not None:
        with open(key_word_list_file, 'r') as fp:
            key_word_list = [l.strip() for l in fp.readlines()]
    else:
        key_word_list = None

    tag_corpus(splits, sentences_json, key_word_list, key_word_pos_list)
    with open(output_json_file, 'w') as fp:
        json.dump(sentences_json, fp, indent=4)
        

def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.register("type", "bool", lambda v: v.lower() == 'true')
    p.add_argument("--split_file", type=str, default=None, help="")
    p.add_argument("--json_file", type=str, default=None, help="")
    p.add_argument("--out_json_file", type=str, default=None, help="")
    p.add_argument("--key_word_list_file", type=str, default="./key_word_list.txt", help="")
    p.add_argument("--key_word_pos_list_file", type=str, default="key_word_pos_list.txt", help="")

    FLAGS, _ = p.parse_known_args()
    print(FLAGS.split_file)
    print(FLAGS.json_file)
    print(FLAGS.out_json_file)
    print(FLAGS.key_word_list_file)
    print(FLAGS.key_word_pos_list_file)
    
    add_word_tag(FLAGS.split_file, 
                 FLAGS.json_file, 
                 FLAGS.out_json_file, 
                 FLAGS.key_word_list_file, 
                 FLAGS.key_word_pos_list_file)
    
