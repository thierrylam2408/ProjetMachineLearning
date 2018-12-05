#!usr/bin/python

import sys
import random

#Variables globals
fields = ["id", "original_title", "overview", "genres"]

# retourne dict genre:id, id = int
def load_genres(filename):
    f = open(filename,"r")
    dict_genre = {}
    for i in f:
        t = i.split(",")
        t[1] = t[1].rstrip()
        dict_genre[t[0]] = t[1]
    return dict_genre

#parse le fichier filename en List de [id, original_title, overview, List[idgenres]]
def getFilms(filename):
	result=[]
	with open(filename, encoding='utf-8') as file:
		for row in file:
			split = row.split("||")
			if(len(split) == len(fields)):
				split[fields.index("genres")] = split[fields.index("genres")][:-1].split(",")
				result.append(split)
	return result

#Recupere le champs d'un film
def getFieldsByIdFilm(idFilm, field, datas):
	for film in [ [ i[fields.index(field)] , i[fields.index("id")] ]  for i in datas]:
		if(int(film[1]) == int(idFilm)):
			return film[0]

#Liste des films qui ont ce genre
def idFilmsByIdGenre(idGenre, datas):
	result = []
	for film in datas:
		if(idGenre in film[fields.index("genres")]):
			result.append(film[fields.index("id")])
	return result
			

def test():
	datas = getFilms("data")
	overview_raw = datas[0][fields.index("overview")]
	print(overview_raw)
	print(getFieldsByIdFilm("601", "genres", datas))
'''
	idFilmsComedy = idFilmsByIdGenre("35", datas)
	print("Il y a "+str(len(idFilmsComedy))+ " films comiques")
	for idF in idFilmsComedy:
		print(getFieldsByIdFilm(idF, "genres", datas))
'''
