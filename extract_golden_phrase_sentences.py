#!/usr/bin/env python
# coding: utf-8
import argparse
import torch
import os
import spacy
import json
import sys
sys.path.append("../")

from flickr30k_entities_utils import get_sentence_data_from_line

def make_golden_phrase_sentence_data(sentences_dir, splits):
    nlp = spacy.load("en_core_web_sm")
    sentence_datas = []
    for split in splits:
        image_file_name = split.strip()
        image_id = image_file_name.split(".")[0]
        
        sentences_path = os.path.join(sentences_dir, image_id+".txt")
        with open(sentences_path, 'r') as fp:
            sentences = [line.strip() for line in fp.readlines()]
        for item in sentences:
            annotated_sentence_item = get_sentence_data_from_line(item.lower())
            annotated_sentence_item['image_id'] = image_file_name
            sentence_datas.append(annotated_sentence_item)
    return sentence_datas
            

def read_data_and_process(sentences_dir, splits_file, output_file):
    with open(splits_file, 'r') as fp:
        splits = fp.readlines()
    
    sentences = make_golden_phrase_sentence_data(sentences_dir, splits)
    for i in range(10):
        print(sentences[i])
    torch.save(sentences, output_file)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.register("type", "bool", lambda v: v.lower() == 'true')
    p.add_argument("--splits_file", type=str, default="/home/xhuang/work/corpus/multi30k/original/splits/train_images.txt", help="")
    p.add_argument("--sentences_dir", type=str, default="/home/xhuang/work/corpus/multi30k/original/Sentences", help="")
    p.add_argument("--output_file", type=str, default="./extra_flickr_golden_phrases_train_sentences.pth", help="")

    FLAGS, _ = p.parse_known_args()
    read_data_and_process(FLAGS.sentences_dir, FLAGS.splits_file, FLAGS.output_file)

