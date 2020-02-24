from flask import Flask
from flask import render_template
import tweepy
import json
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import statistics as st
from textblob import TextBlob

def registrar():
    access_token = "800192874155388929-HjKmhrNlAzJ55GemrHoT0Xtqi9GnlSM"
    access_token_secret = "phlnEgeOqGE04VHu5P0olWAQX6SY5MoVS3XhkS3CTW4cr"
    API_key = "aiw9NAl4eoelHobSRjzvPsxzM"
    API_secret_key = "ngdfIGvF8kcOXOkBHJlylPfpOlLqksBKfBC9NHOaz8pytR6rXk"

    auth = tweepy.OAuthHandler(API_key, API_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def barras(api):
    data1 = api.get_user("Uber_Col")
    dato1 = int(float(data1._json["followers_count"]))
    print(dato1)

    data2 = api.get_user("Picapco")
    dato2 = int(float(data2._json["followers_count"]))
    print(dato2)

    data3 = api.get_user("didicolombia")
    dato3 = int(float(data3._json["followers_count"]))
    print(dato3)

    data4 = api.get_user("cabify_colombia")
    dato4 = int(float(data4._json["followers_count"]))
    print(dato4)

    Data1 = ["Uber", "Picap", "Didi", "Cabify"]
    Data2 = [dato1, dato2, dato3, dato4]

    ypos = np.arange(len(Data1))

    plt.xticks(ypos, Data1)
    plt.bar(ypos, Data2)
    plt.savefig("static/images/barras.png")
    plt.cla()
    plt.clf()

def procentaje(p, t):
    return 100*float(p)/float(t)

def pastel():
    posi = 0
    nega = 0
    neut = 0
    polarity = 0

    tweets = tweepy.Cursor(api.search, q="uber").items(100)

    for tweet in tweets:
        #print(tweet.text)
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity

        if (analysis.sentiment.polarity == 0.00):
            neut += 1
        elif (analysis.sentiment.polarity < 0.00):
                nega += 1
        elif (analysis.sentiment.polarity > 0.00):
                    posi += 1

    posi = procentaje(posi, 100)
    nega = procentaje(nega, 100)
    neut = procentaje(neut, 100)

    posi = format(posi, ".2f")
    nega = format(nega, ".2f")
    neut = format(neut, ".2f")

    if (polarity == 0):
        print("Neutral")
    elif (polarity < 0):
        print("Negativo")
    elif (polarity > 0):
        print("Positivo")

    labels = ["Positivo["+str(posi)+"%]", "Neutral["+str(neut)+"%]", "Negativo["+str(nega)+"%]"]

    sizes = [posi, neut, nega]
    colors =["orange", "blue", "yellow"]
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("static/images/pastel.png")
    plt.show()
    plt.cla()
    plt.clf()
    
def departamento():
        lista = [[tweet.user.location] for tweet in tweepy.Cursor(api.search,screen_name="Uber_col",q="Colombia", tweet_mode="extended").items(100)]
        valores=[0,0,0,0,0]
        for lugar in lista:
            if((lugar[0].find("Bogotá")!=-1)or(lugar[0].find("Bogota")!=-1)or(lugar[0].find("bogotá")!=-1)or(lugar[0].find("bogota")!=-1)):
                valores[0]+=1
            elif((lugar[0].find("Cali")!=-1)or(lugar[0].find("cali")!=-1)):
                    valores[1]+=1
            elif((lugar[0].find("Medellín")!=-1)or(lugar[0].find("Medellin")!=-1)or(lugar[0].find("medellin")!=-1)or(lugar[0].find("medellín")!=-1)):
                    valores[2]+=1
            elif((lugar[0].find("Valledupar")!=-1)or(lugar[0].find("valledupar")!=-1)):
                    valores[3]+=1
            else:
                    valores[4]+=1
        lugares=["Bogotá","Cali","Medellín","Valledupar","Otro"]
        plt.xticks(np.arange(5),lugares)
        plt.bar(np.arange(5),valores)
        plt.savefig("static/images/departamento.png")
        plt.show()
app = Flask(__name__)

api=registrar()
barras(api)
pastel()
departamento()
arreglo= ["","","","",""]
var=0
for tweet2 in tweepy.Cursor(api.search, q="Uber_Col-filter:reetweets", tweet_mode="extended").items(5):
    arreglo[var]=tweet2._json["full_text"]
    var=var+1


@app.route("/")
def index():
    
    return render_template("index.html",arreglo=arreglo)

if(__name__=="__main__"):
    app.run()
