from nltk.translate.bleu_score import SmoothingFunction
from nltk.translate.bleu_score import corpus_bleu
def each_bleu(ref,pred):
    chencherry = SmoothingFunction()
    with open(ref) as fp_ref, open(pred) as fp_pred:
        for ref_line,pred_line in zip(fp_ref,fp_pred):
            bleu = corpus_bleu([[ref_line.split()]], [pred_line.split()], smoothing_function=chencherry.method4,
                               emulate_multibleu=True)*100
            print("ref ",ref_line)
            print("pred ",pred_line)
            print("bleu ",bleu)
            print("\n\n")
    # hyp = "Teo S yb , oe uNb , R , T t , , t Tue Ar saln S , , 5istsi l , 5oe R ulO sae oR R"
    # ref = "Their tasks include changing a pump on the faulty stokehold . Likewise , two species that are very similar in morphology were distinguished using genetics ."