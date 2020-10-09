import bleu
import sys

if __name__ == '__main__':
	hypo_filename = sys.argv[1]
	ref_filename = sys.argv[2]
	result_file = sys.argv[3]
	print(hypo_filename)
	print(ref_filename)
	print(result_file)
	hypo_file = open(hypo_filename, 'rt')
	ref_file = open(ref_filename, 'rt')
	results = []
	for hypo in hypo_file:
		hypo = hypo.strip().split()
		ref = ref_file.readline().strip().split()
		result = bleu.bleu_plus_one([ref], 1, hypo, 4)
		results.append(result)

	with open(result_file, 'w') as fp:
		for r in results:
			fp.write((str(r) + "\n"))

	hypo_file.close()
	ref_file.close()
