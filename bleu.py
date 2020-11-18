#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage:
  bleu.py --reference FILE --translation FILE [--weights STR] [--smooth STR] [--smooth-epsilon STR] [--smooth-alpha STR] [--smooth-k STR] [--segment-level]
  bleu.py -r FILE -t FILE [-w STR] [--smooth STR] [--segment-level]
  
Options:
  -h --help              Show this screen.
  -r --reference FILE    reference file (Complusory)
  -t --translation FILE  hypothesis file (Complusory)
  -w --weights STR       weights [default: 0.25 0.25 0.25 0.25]
  --segment-level        prints segment level scores
  --smooth STR           smoothens segment level scores
  --smooth-epsilon STR   empirical smoothing parameter for method 1 [default: 0.1]
  --smooth-k STR         empirical smoothing parameter for method 4 [default: 5]
  --smooth-alpha STR     empirical smoothing parameter for method 6 [default: 5]
'''

from __future__ import division, print_function

import io
import math
import sys
from fractions import Fraction
from collections import Counter
from functools import reduce
from operator import or_

try:
	from nltk import ngrams
except:
	def ngrams(sequence, n):
		sequence = iter(sequence)
		history = []
		while n > 1:
			history.append(next(sequence))
			n -= 1
		for item in sequence:
			history.append(item)
			yield tuple(history)
			del history[0]


def modified_precision(references, hypothesis, n):
	# Extracts all ngrams in hypothesis.
	counts = Counter(ngrams(hypothesis, n)) 
	if not counts:
		return Fraction(0)
	# Extract a union of references' counts.
	max_counts = reduce(or_, [Counter(ngrams(ref, n)) for ref in references])
	# Assigns the intersection between hypothesis and references' counts.
	clipped_counts = {ngram: min(count, max_counts[ngram]) for ngram, count in counts.items()}
	return Fraction(sum(clipped_counts.values()), sum(counts.values())) 

def modified_precision_plusone(references, hypothesis, n):
	# Extracts all ngrams in hypothesis.
	counts = Counter(ngrams(hypothesis, n)) 
	if not counts:
		return 1.0
	# Extract a union of references' counts.
	max_counts = reduce(or_, [Counter(ngrams(ref, n)) for ref in references])
	# Assigns the intersection between hypothesis and references' counts.
	clipped_counts = {ngram: min(count, max_counts[ngram]) for ngram, count in counts.items()}
	return Fraction(1+sum(clipped_counts.values()), 1+sum(counts.values())) 
    
   
def bleu_plus_one(references,ref_num, hypothesis, ngram_order, print_result=True):
	if len(references) != ref_num:
		return 0.0

	hypo_len = len(hypothesis)

	ref_lens = (len(reference) for reference in references)
	shortest_ref_len = min(ref_lens)
	bp = min(math.exp(1 - shortest_ref_len / hypo_len), 1.0)

	ngram_precisions = [0.0]*ngram_order
	for i in range(ngram_order):
		ngram_precisions[i] = modified_precision_plusone(references, hypothesis, i+1)

	ngram_precisions = [0.25*math.log(p_i) for p_i in ngram_precisions]

	result = bp * math.exp(math.fsum(ngram_precisions))
	if print_result:
		print (result)
	return result


def bleu_corpus_segment(hypo_filename, ref_filename,multi=False):
	hypo_file = open(hypo_filename, "rt")

	if multi==True:
		ref_file1 = open(ref_filename+".1", "rt")
		ref_file2 = open(ref_filename+".2", "rt")
		ref_file3 = open(ref_filename+".3", "rt")
		ref_file4 = open(ref_filename+".4", "rt")
		ref_file5 = open(ref_filename+".5", "rt")
		for hypo in hypo_file:
			hypo = hypo.strip().split()
			ref1 = ref_file1.readline().strip().split()
			ref2 = ref_file2.readline().strip().split()
			ref3 = ref_file3.readline().strip().split()
			ref4 = ref_file4.readline().strip().split()
			ref5 = ref_file5.readline().strip().split()
			ref_list = []
			ref_list.append(ref1)
			ref_list.append(ref2)
			ref_list.append(ref3)
			ref_list.append(ref4)
			ref_list.append(ref5)
			bleu_plus_one(ref_list, 5, hypo, 4)
	else:
		ref_file = open(ref_filename, "rt")
		for hypo in hypo_file:
			hypo = hypo.strip().split()
			ref = ref_file.readline().strip().split()
			ref_list = []
			ref_list.append(ref)
			bleu_plus_one(ref_list, 1, hypo, 4)

	log_file = open("log.txt", "wt")


		

if __name__ == '__main__':
    bleu_corpus_segment(sys.argv[1], sys.argv[2], True)
