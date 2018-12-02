#!usr/bin/python
#nltk
import sys
import csv
import json

#Variables globals
fields = ["genres", "id", "keywords", "original_title", "overview"]
datas = filterByFieldsName("tmdb_5000_movies.csv", fields)

#Selectionne les champs du fichier
def filterByFieldsName(filename, fields):
	result=[]
	with open(filename, encoding='utf-8') as csvfile:
		data = list(csv.reader(csvfile))
		index = [data[0].index(field) for field in fields]
		for row in data[1::]:
			result.append([row[i] for i in index])
	return result

#Dictionnaire idGenre=>NomGenre
def idGenres():
	idGenres = dict()
	for genresPerFilm in [ i[fields.index("genres")] for i in datas]:
		for genreDict in json.loads(genresPerFilm):
			idGenres[genreDict['id']] = genreDict['name']
	return idGenres

#Recupere le champs d'un film
def getFieldsByIdFilm(idFilm, field):
	for film in [ [ i[fields.index(field)] , i[fields.index("id")] ]  for i in datas]:
		if(int(film[1]) == int(idFilm)):
			return film[0]


#Liste des films qui ont ce genre
def idFilmsByIdGenre(idGenre):
	result = []
	for film in [ [ i[fields.index("genres")] , i[fields.index("id")] ]  for i in datas]:
		for genreDict in json.loads(film[0]):
			if(int(genreDict['id']) == idGenre):
				result.append(film[1])
				break
	return result
			

def test():
	print(datas[0][fields.index("overview")])
	print(idGenres())
	print(getFieldsByIdFilm(19995, "overview"))
	idFilmsComedy = idFilmsByIdGenre(35)
	print("Il y a "+str(len(idFilmsComedy))+ " films comiques")
	for idF in idFilmsComedy:
		print(getFieldsByIdFilm(idF, "genres"))
