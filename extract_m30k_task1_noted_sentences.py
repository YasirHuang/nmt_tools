#coding=utf-8
from __future__ import print_function
from flickr30k_entities_utils import get_annotations, get_sentence_data
import os
import json
from tqdm import tqdm
import argparse

def sentence_match(annoted_sentence, sentence):
    dots = {'，':',',
            '’':'\'', 
            '。':'.', 
            '”':'"',
            '“':'"'}
    sent_scores = []
    sentence_len = len(sentence.strip().split())
    for asent in annoted_sentence:
        asent_sent = asent['sentence'].lower().strip().split()
        # check illegal symbols
        for i, w in enumerate(asent_sent):
            if w in dots.keys():
                asent_sent[i] = dots[w]
        asent_sent_len = len(asent_sent)
        sent_len_score = float(sentence_len) / float(asent_sent_len)
        sent_len_score = sent_len_score if sent_len_score <= 1.0 else 1.0/sent_len_score
        
        min_len = min(asent_sent_len, sentence_len)
        max_len = max(asent_sent_len, sentence_len)
        word_match_number = 0
        for asw, w in zip(sentence.lower().strip().split()[:min_len], asent_sent[:min_len]):
            if asw == w:
                word_match_number += 1
        words_match_score = float(word_match_number)/float(max_len)
        score = words_match_score*sent_len_score
        sent_scores.append(score)
    
    max_score_idx = 0
    for i, score in enumerate(sent_scores):
        if score > sent_scores[max_score_idx]:
            max_score_idx = i
            
    return annoted_sentence[max_score_idx], sent_scores[max_score_idx]
        
def test_match(sent_id, split_file, sentence_file, annoted_sentence_dir='./Sentences/'):
    annoted_sent = get_sentence_data(os.path.join(annoted_sentence_dir, "%s.txt"%sent_id))
    
    with open(split_file, 'r') as fp:
        splits = fp.readlines()
        splits = [s.strip().split('.')[0] for s in splits]
        
    with open(sentence_file, 'r') as fp:
        sentences = fp.readlines()
        sentences = [s.strip() for s in sentences]
    split_sent_dict = {}

    for s_id, sent in zip(splits, sentences):
        split_sent_dict[s_id] = sent
    
    ret_annoted_sent, sent_score = sentence_match(annoted_sent, split_sent_dict[sent_id])
    print(annoted_sent)
    print(ret_annoted_sent)
    print(sent_score)
    print(split_sent_dict[sent_id])
#test_match('4641889254', './splits/train_images.txt', '/home/xhuang/work/corpus/Multi30K/task1/train.tok.en')

def extract(split_file, sentence_file, annoted_sentence_dir):
    with open(split_file, 'r') as fp:
        splits = fp.readlines()
        
    with open(sentence_file, 'r') as fp:
        sentences = fp.readlines()
        
    results = {}
    for sent_id, sent in tqdm(zip(splits, sentences)):
        sent_id = sent_id.strip().split('.')[0]
        sent = sent.strip()
        annoted_sent = get_sentence_data(os.path.join(annoted_sentence_dir, "%s.txt"%sent_id))
        selected_annoted_sent, score = sentence_match(annoted_sent, sent)
        if score < 1.0:
            print(sent_id, score)
            print(selected_annoted_sent)
            print(sent)

        results[sent_id] = selected_annoted_sent
    return results



def add_arguments(parser):
    """Build ArgumentParser."""
    parser.register("type", "bool", lambda v: v.lower() == "true")

    parser.add_argument("--split_file", type=str, default="./splits/train_images.txt",
                        help="")
    parser.add_argument("--sentences_file", type=str, default='/home/xhuang/work/prior-img-emb_nmt/experiment/data/train.tok.en',
                        help="")
    parser.add_argument("--annoted_sentence_path", type=str, default="./Sentences/")
    parser.add_argument("--output_file", type=str, default="/home/xhuang/work/prior-img-emb_nmt/experiment/data/train.tok.en.json")


def main(FLAGS):
    results = extract(FLAGS.split_file, 
                      FLAGS.sentences_file, 
                      FLAGS.annoted_sentence_path)
    with open(FLAGS.output_file, 'w') as fp:
        json.dump(results, fp)  


if __name__ == "__main__":
    cc_parser = argparse.ArgumentParser()
    add_arguments(cc_parser)
    FLAGS, unparsed = cc_parser.parse_known_args()
    # tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
    main(FLAGS)
