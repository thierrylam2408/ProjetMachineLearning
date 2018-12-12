import classification
import random
import parseur
import matplotlib.pyplot as plt
import pandas as pd

#cat data_eval | head -50000 > echantillon_eval

#genere deux datasets depuis un dataset complet pour l'entrainement(80%) et l'evaluation(20%)
#Si la ligne ne contient pas toutes les données, on l'ignore
#Retourne le nb de ligne ignoré
def split_lines(input, seed, train_file, eval_file):
	random.seed(seed)
	p1 = open(train_file, "w")
	p2 = open(eval_file, "w")
	nb_filtre = 0
	for line in open(input, "r").readlines():
		tab = line.rstrip().split('||')
		if(len(tab) == 4 and tab[3] != "" and tab[2]!= "" and tab[1] != "" and tab[0] !=""):
			if(random.random() < 0.8):
				p1.write(line)
			else: p2.write(line)
		else: nb_filtre += 1
	return nb_filtre

def naive_bayes_eval_pourcentage_de_bonnes_reponses(data_eval, seuil, data_train):
	predictSuccessfull = 0
	predictTotal = 0
	for data in data_eval:
		if (data[parseur.fields.index("genres")] != [''] and data[parseur.fields.index("overview")] != ""):
			if(idsEnCommun(
				classification.naive_bayes_predict2("genres_file", data_train, data[parseur.fields.index("overview")]),
				data[parseur.fields.index("genres")]) >= seuil):
					print("ok")
					predictSuccessfull = predictSuccessfull + 1
			else: print("pas ok")
			predictTotal = predictTotal + 1
	return predictSuccessfull / predictTotal


def naive_bayes_eval_recall_precision_par_genres(data_eval, data_train):
  genres = parseur.load_genres("genres_file")
  num_predicted_genres = dict.fromkeys(genres, 0)
  num_actual_genres = dict.fromkeys(genres, 0)
  num_actual_and_predicted_genres = dict.fromkeys(genres, 0)
  recalls_precisions = []
  for data in data_eval:
    if (data[parseur.fields.index("genres")] != [''] and data[parseur.fields.index("overview")] != ""):
      predicts = classification.naive_bayes_predict2("genres_file", data_train, data[parseur.fields.index("overview")])
      for genre in parseur.load_genres("genres_file"):
        if genre in predicts:
          num_predicted_genres[genre] += 1
          if genre in data[parseur.fields.index("genres")]:
            num_actual_and_predicted_genres[genre] += 1
        if genre in data[parseur.fields.index("genres")]:
          num_actual_genres[genre] += 1
  return [ (genre, num_actual_and_predicted_genres[i] / num_actual_genres[i] if num_actual_genres[i] else 1.0,
  	num_actual_and_predicted_genres[i] / num_predicted_genres[i] if num_predicted_genres[i] else 1.0) for (i,genre) in genres.items() ]


#pourcentage de bonnes predictions par rapport aux veritables genres
def idsEnCommun(ids_pred, ids_eval):
	print("IdsGenre prédit:")
	print(*ids_pred)
	print("IdsGenre en vrai:")
	print(*ids_eval)
	return len([i for i in ids_pred if i in ids_eval]) / len(ids_eval)
def generate_histo(title, values):

	X = []
	Y = []
	Z = []

	for i in values:
		X.append(i[0])
		Y.append(i[1])
		Z.append(i[2])
		df = pd.DataFrame(np.c_[Y,Z], index=X)
	df.plot.bar()

	plt.show()

def test():
	#print(idsEnCommun(["41","1","6","8","2","411"], ["6","411", "2"])) #tous les genres sont trouves

	#print(split_lines("data", 30, "data_train", "data_eval"))
	data_eval = parseur.getFilms("echantillon_eval")
	data_train = "echantillon_train"
	seuil = 2/3
	#print("avec un seuil de "+str(seuil)+" on a "+ str(naive_bayes_eval_pourcentage_de_bonnes_reponses(data_eval, seuil,data_train)*100)+"% de reussite")
	print(naive_bayes_eval_recall_precision_par_genres(data_eval, data_train))
