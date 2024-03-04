#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Kendahl Toft
#Project 1 Milestone 3 Data Analysis
#Date Created: 9/10/2023
#Date Modified: 9/21/2023
import requests
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob
#gets website html
x = requests.get('https://www.theonion.com/latest')
#creating variables for later use
text=""
titles=[]
site=""
wordAmount = []
badArticles=0
goodArticles=0
neutralArticles=0
sentiment=0
articleNum="somethin"
#simple loop to confirm article number
while(articleNum.isdigit()==False):
    articleNum=input("How many articles to read in?")
    if(articleNum.isdigit()==False):
        print("Needs to be a Number")
    elif(int(articleNum)<0):
        print("Needs to be a positive Number")
    else:
        articleNum=int(articleNum)
        break
#code to run through the first page and gather article information
for c in x.iter_lines():
    #decodes each line from utf-8
    c=c.decode('utf-8')
    #searches for the article tag in html
    if('<article' in c):
        #searches for this specific tag inside the article tag which contains the href link that we need
        while c.find("sc-cw4lnv-5 dYIPCV")>0:
            word=c.partition("sc-cw4lnv-5 dYIPCV")
            c=word[2]
            temp=c.find('href="')+6
            site=c[temp:c.find('"',temp)]
            y=requests.get(site)
            #checks to see if we have reached our article number before running the loop to seach through articl html
            if(articleNum>0):
                for search in y.iter_lines():
                    search=search.decode('utf-8')
                    #finds the title tag of the article and adds it to a list
                    if("<title>" in search):
                        titles.append(search[search.find("<title>")+7:search.find("</title>")])
                    #finds the body text in the article and adds it to a string
                    if("<p" in search):
                        temp = search.find("<p class")
                        templist=search[search.find('>',temp)+1:search.find("</p>")]
                        templist=templist.split(" ")
                        #finds the length of each article for the list
                        if(len(templist)>1):
                            wordAmount.append(len(templist))
                        #finds sentiment of paragraph
                        sentiment=TextBlob(search[search.find('>',temp)+1:search.find("</p>")]).sentiment.polarity
                        text=text+" "+search[search.find('>',temp)+1:search.find("</p>")]
                if(sentiment<0):
                    titles.append(sentiment)
                    titles.append("Bad Article")
                    badArticles=badArticles+1
                elif(sentiment==0):
                    titles.append(sentiment)
                    titles.append("Neutral Article")
                    neutralArticles=neutralArticles+1
                else:
                    titles.append(sentiment)
                    titles.append("Good Article!")
                    badArticles=badArticles+1
                        
                articleNum=articleNum-1
#this loop goes through the next page if we haven't reached our article number
while(articleNum>0):
    for c in x.iter_lines():
        c=c.decode('utf-8')
        num=c.find('href="?star')
        temp=c.find('href="?star')+6
        if(num>0):
            site=c[temp:c.find('"',temp)]
            #fun little code to go to the next page by adding the href under the button to the current page
            site="https://www.theonion.com/latest"+site
    x=requests.get(site)
    for c in x.iter_lines():
        c=c.decode('utf-8')
        if('<article' in c):
            while c.find("sc-cw4lnv-5 dYIPCV")>0:
                word=c.partition("sc-cw4lnv-5 dYIPCV")
                c=word[2]
                temp=c.find('href="')+6
                site=c[temp:c.find('"',temp)]
                y=requests.get(site)
                if(articleNum>0):
                    for search in y.iter_lines():
                        search=search.decode('utf-8')
                        if("<title>" in search):
                            titles.append(search[search.find("<title>")+7:search.find("</title>")])
                        if("<p" in search):
                            temp = search.find("<p class")
                            templist=search[search.find('>',temp)+1:search.find("</p>")]
                            templist=templist.split(" ")
                            if(len(templist)>1):
                                wordAmount.append(len(templist))
                            #finds sentiment of the paragraph
                            sentiment=TextBlob(search[search.find('>',temp)+1:search.find("</p>")]).sentiment.polarity
                            text=text+" "+search[search.find('>',temp)+1:search.find("</p>")]
                    #checks and appends sentiment
                    if(sentiment<0):
                        titles.append(sentiment)
                        titles.append("Bad Article")
                        badArticles=badArticles+1
                    elif(sentiment==0):
                        titles.append(sentiment)
                        titles.append("Neutral Article")
                        neutralArticles=neutralArticles+1
                    else:
                        titles.append(sentiment)
                        titles.append("Good Article!")
                        goodArticles=goodArticles+1
                    articleNum=articleNum-1
#makes a badwords list
badwords=['em']
#populates list with stopwords from kaggle
f= open("stopwords.txt", "r")
for x in f:
    badwords.append(x[:-1])
text=text.strip()
textList=text.split(" ")
#removes extra space
while '' in textList:
    textList.remove('')
#finds mean
mean=len(textList)/20
print("Title List is",titles)
print("Mean Word Number =",mean)
wordAmount.sort()
#finds median
print("Median Word Number =",wordAmount[int(len(wordAmount)/2)])
#prints if articles were mostly good or bad
if(badArticles>goodArticles):
    print("Mostly Negative News")
elif(badArticles<goodArticles):
    print("Mostly Positive News")
else:
    print("Neutral News Today")
#creates wordcloud
wordcloud=WordCloud(max_words=50, stopwords=badwords, background_color="white").generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
#removes stopwords from list
for x in badwords:
    while x in textList:
        textList.remove(x)
#finds frequency of 15 most common words
Frequency = Counter(textList).most_common(15)
x=[i[0]for i in Frequency]
y=[i[1]for i in Frequency]
#creates bar graph
plt.bar(x,y)
plt.xticks(rotation=90)
plt.title('Frequency of words in chosen articles')
plt.ylabel('Frequency')
plt.xlabel('Words')


# In[ ]:





# In[ ]:




