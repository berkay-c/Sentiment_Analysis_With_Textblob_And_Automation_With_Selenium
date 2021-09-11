import pandas as pd
import string
import warnings
from textblob import TextBlob,Word
from googletrans import Translator
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from MainApp import ProgressBarThread





def WordCountLimitation():
    # Limit of 4999 Characters Per Comment
    dataToBeAnalyzed.Comments=dataToBeAnalyzed.Comments.str[:4999]


def translateTrtoEn():
    # Case Conversion
    dataToBeAnalyzed.Comments= dataToBeAnalyzed.Comments.astype(str).apply(lambda x: " ".join(x.lower() for x in x.split()))
    translator = Translator()
    dataToBeAnalyzed['Comments_Eng'] = dataToBeAnalyzed['Comments'].astype(str).apply(lambda x: translator.translate(x, src='tr', dest='en').text)
    


def dataCleaning():
    warnings.filterwarnings("ignore")
    # Remove Punctuations
    dataToBeAnalyzed.Comments=dataToBeAnalyzed.Comments.str.replace('[{}]'.format(string.punctuation), '')
    # Remove numbers
    dataToBeAnalyzed.Comments=dataToBeAnalyzed.Comments.str.replace('\d+','')
    # Fixed a Few Misspellings
    dataToBeAnalyzed.Comments=dataToBeAnalyzed.Comments.str.replace('cok','çok')
    dataToBeAnalyzed.Comments=dataToBeAnalyzed.Comments.str.replace('İyiydi','iyiydi')
    dataToBeAnalyzed.Comments=dataToBeAnalyzed.Comments.str.replace('kotu','kötü')
    # Call 'translateTrtoEn' Function
    translateTrtoEn()
    # Let's use nltk('stopwords') for better sentiment analysis
    # StopWords
    nltk.download('stopwords') 
    stopWords = stopwords.words('english')
    dataToBeAnalyzed.Comments_Eng= dataToBeAnalyzed.Comments_Eng.astype(str).apply(lambda x: " ".join(x for x in x.split() if x not in stopWords))
    # Lemmatization
    nltk.download('wordnet') 
    dataToBeAnalyzed.Comments_Eng= dataToBeAnalyzed.Comments_Eng.astype(str).apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()])) 
    


def getWordCloud_English():
    plt.figure()
    plt.figure(figsize=(8,6))
    allWords_En = ''.join([com for com in dataToBeAnalyzed['Comments_Eng'] ])
    wordCloud_En=WordCloud(width=500,height=400,random_state=21,max_font_size=119).generate(allWords_En)
    plt.imshow(wordCloud_En,interpolation="bilinear")
    plt.axis("off")
    plt.savefig("getWordCloud_English.png")
    print("English Word Cloud Saved as 'getWordCloud_English.png'")


def getPlotThePolarityAndSubjectivity():
    plt.style.use("fivethirtyeight")
    plt.figure(figsize=(8,7))
    for i in range (0,dataToBeAnalyzed.shape[0]):
        plt.scatter(dataToBeAnalyzed.Polarity[i], dataToBeAnalyzed.Subjectivity[i], color = 'Red')
    plt.title("Sentiment Analysis")
    plt.xlabel("Polarity")
    plt.ylabel('Subjectivity')
    plt.savefig("PlotThePolarityAndSubjectivity.png")
    print("Graph of The Polaritiy And Subjectivity Saved as 'PlotThePolarityAndSubjectivity.png'")
    print("-"*50)


def getPlotAndVisualizeTheCounts():
    plt.figure()
    plt.figure(figsize=(8,6))
    plt.title("Sentiment Analysis")
    plt.xlabel("Sentiment")
    plt.ylabel("Counts")
    dataToBeAnalyzed['Analysis'].value_counts().plot(kind="bar")
    plt.savefig("SentimentAnalysisCounts.png")  
    print("Graph of Sentiment Analysis Counts Saved as 'SentimentAnalysisCounts.png'")
        

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity


def getAnalysis(score):
    if  score<0:
        return "Negative"
    elif score == 0 :
        return "Neutral"
    else:
        return "Positive"

    
def creatingAColumnOfAnalysisAndSubjectivityAndPolarity():
    # Create  New Columns
    dataToBeAnalyzed['Subjectivity'] = dataToBeAnalyzed['Comments_Eng'].apply(getSubjectivity)
    dataToBeAnalyzed['Polarity'] = dataToBeAnalyzed['Comments_Eng'].apply(getPolarity)
    dataToBeAnalyzed['Analysis'] = dataToBeAnalyzed['Polarity'].apply(getAnalysis)
    polarityMean=dataToBeAnalyzed["Polarity"].mean()
    PolarityMeanAnalysis=getAnalysis(polarityMean)
    print(f"\nAverage polarity value of comments made = {polarityMean}  and Analysis = {PolarityMeanAnalysis}\n")
    print("-"*50)
    
    
if __name__ == '__main__':
    
        pb_thread = ProgressBarThread('Reading And Cleaning Data')
        pb_thread.start()
        
        dataToBeAnalyzed=pd.read_csv("DataForSentimentAnalysis.csv")
        WordCountLimitation()
        dataCleaning()
        
        pb_thread.stop()
        
        creatingAColumnOfAnalysisAndSubjectivityAndPolarity()
        getPlotAndVisualizeTheCounts()
        getWordCloud_English() 
        getPlotThePolarityAndSubjectivity()
      
        
