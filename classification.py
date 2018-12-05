import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# retourne dict genre:id, id = int
def load_genres(filename):
    f = open(filename,"r")
    dict_genre = {}
    for i in f:
        t = i.split(",")
        t[1] = t[1].rstrip()
        dict_genre[t[0]] = t[1]
    return dict_genre

# retourne liste de mots "utile"
def process_words(overview):
    tokens = word_tokenize(overview)
    stop_words = set(stopwords.words('english'))
    words = [w for w in tokens if w.isalpha() and w not in stop_words] # enléve ponctuation + stop_words
    return words

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
    print(genre_list)
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
    genre_list = load_genres(genre_file)
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

# prédit pour 1 overview
def naive_bayes_predict(genre_file,movie_file,overview):
    c = all_training(genre_file,movie_file)
    words = c[0]
    classifier_dict = c[1] #  genre:[ratio,y_genre,n_genre]
    genre_dict = load_genres(genre_file)

    tmp_list = process_words(overview)
    print(tmp_list)

    words_list = []
    for i in tmp_list:
        if i in words:
            words_list.append(words[i])

    print(words_list)

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
            print("Type " + genre + " n° " + str(i) + ": OUI")
        else:
            print("Type " + genre + ": NON")


def test():
	test1 = "After a gentle alien becomes stranded on Earth, the being is discovered and befriended by a young boy named Elliott. Bringing the extraterrestrial into his suburban California house, Elliott introduces E.T., as the alien is dubbed, to his brother and his little sister, Gertie, and the children decide to keep its existence a secret. Soon, however, E.T. falls ill, resulting in government intervention and a dire situation for both Elliott and the alien."
	test2 = "Gellert Grindelwald has escaped imprisonment and has begun gathering followers to his cause—elevating wizards above all non-magical beings. The only one capable of putting a stop to him is the wizard he once called his closest friend, Albus Dumbledore. However, Dumbledore will need to seek help from the wizard who had thwarted Grindelwald once before, his former student Newt Scamander, who agrees to help, unaware of the dangers that lie ahead. Lines are drawn as love and loyalty are tested, even among the truest friends and family, in an increasingly divided wizarding world."
	test3 = "On July 2, a giant alien mothership enters orbit around Earth and deploys several dozen saucer-shaped 'destroyer' spacecraft that quickly lay waste to major cities around the planet. On July 3, the United States conducts a coordinated counterattack that fails. On July 4, a plan is devised to gain access to the interior of the alien mothership in space, in order to plant a nuclear missile."
	naive_bayes_predict("genres_file","data",test1)
