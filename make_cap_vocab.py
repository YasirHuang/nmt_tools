import cPickle as pickle
import numpy as np
corpus_dir = "/home/xhuang/work/corpus/Multi30K/"
corpus_sent = "test2016.tok.truecase.en"
corpus_feat = "flickr30k_test_bninception_cnn_features.npy"
sentences = []
sent_len = []
len_sent_dict = {}

path = "/home/xhuang/work/CNN-LSTM-Caption-Generator/"
with open("/home/xhuang/work/CNN-LSTM-Caption-Generator/data_files/index2token.pkl", "r") as f :
	token_dict = pickle.load(f)
	token_idict = {v:k for k,v in zip(token_dict.keys(), token_dict.values())}
	sos_id = token_idict['<SOS>']
	eos_id = token_idict['<EOS>']
	with open(corpus_sent, "r") as f2:
		line = f2.readline()
		while line:
			tokens = line.split()
			tokens_id = [sos_id]
			for t in tokens:
				if token_idict.has_key(t):
					tokens_id.append(token_idict[t])
				else:
					tokens_id.append(token_idict['<UKN>'])
			tokens_id.append(eos_id)
			sentences.append(tokens_id)
			sent_len.append(len(tokens_id))
			line = f2.readline()
	
	feat = np.load(corpus_dir + corpus_feat)
	sent_dict = {}
	img_dict = {}
	indexes = []
	for i,s in enumerate(sentences):
		sent_dict[i]=s
		img_dict[i]=i
		indexes.append(i)
	lens = list(set(sent_len))
	print lens
	
	indexes = np.array(indexes)
	for l in lens:
		index = [np.array(sent_len) == l]
		len_sent_dict[l] = set(indexes[index])

	with open("preprocessed_test_caption.pkl", "w+") as f3:
		pickle.dump((len_sent_dict, sent_dict, img_dict), f3)
		#pickle.dump(sent_dict, f3)
		#pickle.dump(img_dict, f3)

	feat_dict = {}
	for i, ff in enumerate(feat):
		feat_dict[i] = ff
	with open("test_image_id2feature.pkl", "w") as f4:
		pickle.dump(feat_dict, f4)
