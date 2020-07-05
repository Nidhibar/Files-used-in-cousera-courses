

#QUESTION: Define a function get_sorted_recommendations. It takes a list of movie titles as an input. It returns a sorted list of related movie titles as output, up to five related movies for each input movie title. The movies should be sorted in descending order by their Rotten Tomatoes rating, as returned by the get_movie_rating function. Break ties in reverse alphabetic order, so that ‘Yahşi Batı’ comes before ‘Eyyvah Eyvah’.
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_related_titles(["Black Panther", "Captain Marvel"])
# get_related_titles([])
#Doesnt work without the key!!!
import requests_with_caching
import json
def get_movies_from_tastedive(mov):
    d={}
    baseurl="https://tastedive.com/api/similar"
    d['q']=mov
    d["type"]="movies"
    d["limit"]="5"
    resp=requests_with_caching.get(baseurl,params=d)
    #print(resp.text)
    r=json.loads(resp.text)
    return r
def extract_movie_titles(d):
    l=d["Similar"]["Results"]
    l2=[]
    for i in l:
        l2.append(i["Name"])
    return l2

def get_related_titles(l):
    l2=[]
    for movie in l:
        g=get_movies_from_tastedive(movie)
        e=extract_movie_titles(g)
        for name in e:
            if name not in l2:
                l2.append(name)
    return l2


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_movie_rating(get_movie_data("Deadpool 2"))
import json
import requests_with_caching
def get_movie_data(title):
    baseurl="http://www.omdbapi.com/"
    d={"r":"json","t":title}
    resp=requests_with_caching.get(baseurl,params=d)
    di=json.loads(resp.text)
    return di
def get_movie_rating(d):
    '''if len(d['Ratings']) > 1:
        if d['Ratings'][1]['Source']=='Rotten Tomatoes':
            ro=d['Ratings'][1]['Value'][:2]
            ro=int(ro)
            #print(r)
    else:
        ro=0
    
    return ro'''
    strRating=""
    for typeRatingList in d["Ratings"]:
        if typeRatingList["Source"]== "Rotten Tomatoes":
            strRating = typeRatingList["Value"]
    if strRating != "":
        rating = int(strRating[:2])
    else: rating = 0
    return rating

def get_sorted_recommendations(listMovieTitle):
    listMovie= get_related_titles(listMovieTitle)
    listMovie= sorted(listMovie, key = lambda movieName: (get_movie_rating(get_movie_data(movieName)), movieName), reverse=True)
    
    return listMovie
#print(get_movie_rating(get_movie_data("Deadpool 2")))
