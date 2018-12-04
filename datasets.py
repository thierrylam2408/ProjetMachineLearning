import json
import requests
import time

# lit fichier movie_ids.json et récupére une liste des id de films
# fichier fourni par le site tmdb
def get_ids(index_file):
    file = open(index_file, "r")
    ids_list = []
    for i in file:
        x = json.loads(i)
        ids_list.append(x['id'])
    return ids_list

# récupére la liste des genre de films existant sur le site tmdb
# renvoit dict, key = id (entier), value = genre
# écrit les genres dans le fichier output au format: id,genre
def get_genres(output, v3_key):
    params = {"api_key":v3_key}
    f = open(output,"w+")
    r = requests.get('https://api.themoviedb.org/3/genre/movie/list', params=params)
    list_genres = r.json()['genres']
    genres = {}
    for i in list_genres:
        genres[i['id']] = i['name']
        f.write(str(i['id']) + "," + i['name'] + "\n")
    return genres

# écrit dans f les données du film, movie_data = json envoyé par le serveur
# id|nom|résumé|genre1,genre2,...
def write_data(f, movie_data,id):

    list_genres = movie_data['genres']
    chaine_genre = ""
    for i in list_genres:
        chaine_genre = chaine_genre + str(i['id']) + ","
    chaine_genre = chaine_genre[:-1] + '\n'

    title = movie_data['title']
    overview = movie_data['overview']

    f.write(str(id) + "||" + title + "||" + overview + "||" + chaine_genre )

# écrit les données récupérées dans output
# ids_file: fichier contenant les id de tous les films (fichier fourni par tmdb)
# tmp_file: fichier où l'on écrit la valeur de cpt, pour pouvoir reprendre la lors d'une autre execution
def get_db( start,output, ids_file, v3_key, tmp_file):
    file = open(output, "a+")
    tmp = open(tmp_file, "w+")
    params = {"api_key":v3_key}
    cpt = start
    url = "https://api.themoviedb.org/3/movie/"
    list_ids = get_ids(ids_file)
    list_ids = list_ids[start:]

    for i in list_ids:
        r = requests.get( url+str(i) , params=params)
        write_data(file,r.json(),i)
        cpt+=1
        tmp.seek(0)
        tmp.write(str(cpt))
        remaining = int(r.headers['X-RateLimit-Limit'])
        before_reset =  int(r.headers['X-RateLimit-Reset'])
        print("Cpt: " + str(cpt) )
        if(remaining == 0):
            print("Attente de " + str(before_reset) + " sec...")
            time.sleep(before_reset)

v3_key = "7b7aa2e7f1e8697d534123f9abacd1b2"
get_genres("genres_file",v3_key)
get_db(0,"data","movie_ids.json", v3_key , "tmp" )
