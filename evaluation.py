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

def naive_bayes_eval(data_eval):
	predictSuccessfull = 0
	predictTotal = 0
	predictMiss = 0
	for data in data_eval:
		if(idsInCommon( 
			classification.naive_bayes_predict("genres_file","data_train",data[parseur.fields.index("overview")]), 
			data[parseur.fields.index("genres")]) > 0.5):
				print("ok")
				predictSuccessfull = predictSuccessfull + 1
		else: print("pas ok")

#pourcentage de bonnes predictions par rapport aux veritables genres
def idsInCommon(ids_pred, ids_eval):
	print("IdsGenre prédit:")
	print(*ids_pred)
	print("IdsGenre en vrai:")
	print(*ids_eval)
	return len([i for i in ids_pred if i in ids_eval]) / len(ids_eval)

def test():
	#print(idsInCommon(["41","1","6","8","2"], ["6","411", "2"]))
	split_lines("data", 30, "data_train", "data_eval")
	data_eval = parseur.getFilms("tmp")
	naive_bayes_eval(data_eval)
	