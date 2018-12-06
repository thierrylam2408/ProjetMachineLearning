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

def naive_bayes_eval_pourcentage_de_bonnes_reponses(data_eval, seuil):
	predictSuccessfull = 0
	predictTotal = 0
	for data in data_eval:
		if(idsInCommon( 
			classification.naive_bayes_predict("genres_file","data_train", data[parseur.fields.index("overview")]), 
			data[parseur.fields.index("genres")]) > seuil):
				print("ok")
				predictSuccessfull = predictSuccessfull + 1
		else: print("pas ok")
		predictTotal = predictTotal + 1
	return predictSuccessfull / predictTotal


def naive_bayes_eval_recall_precision_par_genres(data_eval):
  genres = parseur.load_genres("genres_file")
  num_predicted_genres = dict.fromkeys(genres, 0)
  num_actual_genres = dict.fromkeys(genres, 0)
  num_actual_and_predicted_genres = dict.fromkeys(genres, 0)
  recalls_precisions = []
  for data in data_eval:
    predicts = classification.naive_bayes_predict("genres_file", "data_train", data[parseur.fields.index("overview")])
    for genre in parseur.load_genres("genres_file"):
      if genre in predicts:
        num_predicted_genres[genre] += 1
        if genre in data[parseur.fields.index("genres")]:
          num_actual_and_predicted_genres[genre] += 1
      if genre in data[parseur.fields.index("genres")]:
        num_actual_genres[genre] += 1
  return [ (num_actual_and_predicted_genres[i] / num_actual_genres[i] if num_actual_genres[i] else 1.0,
  	num_actual_and_predicted_genres[i] / num_predicted_genres[i] if num_predicted_genres[i] else 1.0) for i in genres.keys() ]


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
	data_eval = parseur.getFilms("echantillon_eval")
	seuil = 0.5
	#print("avec un seuil de "+str(seuil)+" on a "+ str(naive_bayes_eval_pourcentage_de_bonnes_reponses(data_eval, seuil))+" de reussite")
	print(naive_bayes_eval_recall_precision_par_genres(data_eval))
	