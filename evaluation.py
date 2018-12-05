import classification
import random
import parseur

#genere deux datasets depuis un dataset complet pour l'entrainement et l'evaluation
def split_lines(input, seed, output1, output2):
	random.seed(seed)
	p1 = open(output1, "w")
	p2 = open(output2, "w")
	for line in open(input, "r").readlines():
		if(random.random() > 0.5):
			p1.write(line)
		else: p2.write(line)

def naive_bayes_eval(file_eval, f):
	predictGenresSuccessfull = 0
	predictGenresTotal = 0
	predictGenresMiss = 0
	#for line in open()

def test():
	split_lines("data", 30, "data_train", "data_eval")
	data_eval = parseur.getFilms("data_eval")
	print(data_eval[0][parseur.fields.index("overview")])