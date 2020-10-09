# coding=utf-8
import tensorflow as tf
import os
import numpy as np
from tensorflow.python import pywrap_tensorflow  
#checkpoint_path = os.path.join(model_dir, "model.ckpt")  
checkpoint_path = tf.train.latest_checkpoint("/home/xhuang/work/datt/experiment/model/bpe_datt_regulation0.003.1/")
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)  
var_to_shape_map = reader.get_variable_to_shape_map()  
for key in var_to_shape_map:  
	#if key.find("Inception"):
	if key.find("Adam") > 0:
		continue
	print("tensor_name: ", key)  
	print(reader.get_tensor(key))
	#print(np.shape(reader.get_tensor(key)))
