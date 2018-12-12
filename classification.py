import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import parseur
import operator

# retourne liste de mots "utile"
def process_words(overview):
    porter = PorterStemmer()
    tokens = word_tokenize(overview)
    stop_words = set(stopwords.words('english'))
    words = [w.lower() for w in tokens if w.isalpha() and w not in stop_words] # enléve ponctuation + stop_words + minuscule
    stemmed = [porter.stem(word) for word in words]
    return stemmed

# format du fichier: id||titre||overview||genre1,genre2...
# format d'un film (id,titre,[mot1,mot2...],[genre1,genre2...])
# l0 => liste des films ayant label dans leur liste de genre
# l1 => liste des films n'ayant pas label dans leur liste de genre
# retourne words => index des mots et ratio_dict => list des elt qui sont du type, et ceux qui ne le sont pas, pour chaque type: {type:(l0,l1)}
def load_data(filename,genre_list):
    f = open(filename,"r")
    words = {}
    last_index = 0
    ratio_dict = {} # genre:(l0,l1) pour chaque genre
    for i in genre_list:
        ratio_dict[i] = ([],[])
    #print(genre_list)
    for i in f:
        i = i.rstrip()
        tab = i.split('||')
        if len(tab) == 4 and tab[3] != "" and tab[2]!= "" and tab[1] != "" and tab[0] !="":
        # faire traitement sur tab[2] ici
            list_words = process_words(tab[2])
            int_words = [] # contient list_words converti en int grace à l'index words
            for j in list_words:
                if j in words: # mot déja dans l'index
                    int_words.append(words[j])
                else:
                    words[j] = last_index
                    int_words.append(last_index)
                    last_index += 1

            genres = tab[3].split(",")
            t = (tab[0],tab[1],int_words,genres)

            for i in genre_list:
                if i in genres:
                    (ratio_dict[i])[0].append(t)
                else:
                    (ratio_dict[i])[1].append(t)
    return (words,ratio_dict)

# pour chaque mot, retourne sa fréquence dans liste_movie
# retourne liste de taille num_words contenant les frequences
def compute_frequencies(num_words, liste_movie):
    freq = [0] * num_words
    for i in liste_movie:
        overview = i[2]
        tmp = set(overview)
        for j in tmp:
            freq[j] += 1
    for k in range(len(freq)):
        freq[k] = float(freq[k]/len(liste_movie))
    return freq

# entraine classifier pour un genre de film donnée
# x = (words,l0,l1)
def naive_bayes_train(x):

    ratio = float(len(x[1])/ (len(x[1])+ len(x[2]))) # ratio de film contenant ce genre dans le dataset => P(genre)

    spamicity = [0] * len(x[0])
    no_spamicity = [0] * len(x[0])
    s = compute_frequencies(len(x[0]),x[1]) # frequence d'apparition des mots dans les films qui ont le genre ciblé => P(word|genre)
    s1 = compute_frequencies(len(x[0]),x[2])
    all_sms = compute_frequencies(len(x[0]),x[1]+x[2]) # fréquence d'apparition des mots dans l'ensemble des films du dataset => P(word)

    for i in range(len(x[0])):
        spamicity[i] = float(s[i]/all_sms[i]) # P(word|genre) / P(word)
        no_spamicity[i] = float(s1[i]/all_sms[i]) # P(word| (not)genre) / P(word)
    return (ratio,spamicity,no_spamicity)



# entraine 1 classifier pour chaque genre
def all_training(genre_file,movie_file):
    genre_list = parseur.load_genres(genre_file)
    x = load_data(movie_file,genre_list)
    words = x[0]

    #  genre:[ratio,y_genre,n_genre]
    classifier_dict = {}

    # entrainement de tous les classifer
    for i in genre_list:
        l0 = x[1][i][0]
        l1 = x[1][i][1]
        t = naive_bayes_train((words,l0,l1))
        classifier_dict[i] = [t[0],t[1],t[2]]
    return (words,classifier_dict)


c = None
# prédit pour 1 overview
#on garde les p_y > p_n
def naive_bayes_predict1(genre_file,movie_file,overview):
    global c
    if(c == None ):
        c = all_training(genre_file,movie_file)
    words = c[0]
    classifier_dict = c[1] #  genre:[ratio,y_genre,n_genre]
    genre_dict = parseur.load_genres(genre_file)

    tmp_list = process_words(overview)
    #print(tmp_list)

    words_list = []
    for i in tmp_list:
        if i in words:
            words_list.append(words[i])

    #print(words_list)
    genres_result = []
    for i in classifier_dict:

        p_y = 1 # proba que l'overview appartienne au genre i
        p_n = 1 # proba que l'overview n'appartienne pas au genre i

        genre_ratio = (classifier_dict[i])[0]
        y_genre = (classifier_dict[i])[1]
        n_genre = (classifier_dict[i])[2]
        for j in words_list:
            p_y = float(p_y * y_genre[j])
            p_n = float(p_n * n_genre[j])
        p_y = p_y*genre_ratio
        p_n = p_n*(1-genre_ratio)
        genre = genre_dict[i]
        if p_y > p_n:
            genres_result.append(str(i))
    return genres_result

#on ordonne pour chaque genre, leur p_n et on garde les 3 plus petites
def naive_bayes_predict2(genre_file,movie_file,overview):
    global c
    if(c == None ):
        c = all_training(genre_file,movie_file)
    words = c[0]
    classifier_dict = c[1] #  genre:[ratio,y_genre,n_genre]
    genre_dict = parseur.load_genres(genre_file)

    tmp_list = process_words(overview)
    #print(tmp_list)

    words_list = []
    for i in tmp_list:
        if i in words:
            words_list.append(words[i])

    #print(words_list)
    genres_prob = dict()
    genres_result = []
    for i in classifier_dict:

        p_y = 1 # proba que l'overview appartienne au genre i
        p_n = 1 # proba que l'overview n'appartienne pas au genre i

        genre_ratio = (classifier_dict[i])[0]
        y_genre = (classifier_dict[i])[1]
        n_genre = (classifier_dict[i])[2]
        for j in words_list:
            p_y = float(p_y * y_genre[j])
            p_n = float(p_n * n_genre[j])
        p_y = p_y*genre_ratio
        p_n = p_n*(1-genre_ratio)
        genre = genre_dict[i]
        genres_prob[str(i)] = p_n
    genres_prob = sorted(genres_prob.items(), key=operator.itemgetter(1))
    genres_prob = list(filter(lambda a: a[1] != 0, genres_prob))
    return [couple[0] for couple in genres_prob[0:3]]


def test():
    #train
    test1 = "After a gentle alien becomes stranded on Earth, the being is discovered and befriended by a young boy named Elliott. Bringing the extraterrestrial into his suburban California house, Elliott introduces E.T., as the alien is dubbed, to his brother and his little sister, Gertie, and the children decide to keep its existence a secret. Soon, however, E.T. falls ill, resulting in government intervention and a dire situation for both Elliott and the alien."
	#eval
    test2 = "Steve Freeling lives with his wife, Diane, and their three children, Dana, Robbie, and Carol Anne, in Southern California where he sells houses for the company that built the neighborhood. It starts with just a few odd occurrences, such as broken dishes and furniture moving around by itself. However, when he realizes that something truly evil haunts his home, Steve calls in a team of parapsychologists led by Dr. Lesh to help before it's too late."
    test3 = "In April of 1945, Germany stands at the brink of defeat with the Russian Army closing in from the east and the Allied Expeditionary Force attacking from the west. In Berlin, capital of the Third Reich, Adolf Hitler proclaims that Germany will still achieve victory and orders his generals and advisers to fight to the last man. When the end finally does come, and Hitler lies dead by his own hand, what is left of his military must find a way to end the killing that is the Battle of Berlin, and lay down their arms in surrender."
    #print(naive_bayes_predict("genres_file","data_train",test3))
    load_data("echantillon_train", "genres_file")