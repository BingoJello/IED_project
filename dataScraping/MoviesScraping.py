#!/usr/bin/env python
# coding: utf-8

# In[133]:


from bs4 import BeautifulSoup as soup, BeautifulSoup  # HTML data structure
from urllib.request import urlopen as uReq, Request, urlopen  # Web client
import csv


# In[134]:


def scrapMoviesByGenre(genre):
    year = ["2000","2001","2002","2003","2004","2005","2006",
            "2007","2008","2009","2010","2011","2012","2013","2014","2015"]
    # open the file in the write mode
    fileName = "data/movies_" + genre + ".csv"
    f = open(fileName, 'w')
    # create the csv writer
    writer = csv.writer(f)
    writer.writerow(["Id","Title","Distributor","Genre"])
    for y in year:
        site= "https://www.the-numbers.com/market/" + y + "/genre/" + genre
        print(site)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        page_soup = BeautifulSoup(page)
        page.close()

        containers = page_soup.findAll("div", {"id": "page_filling_chart"})
        table = containers[1].find("table")
        tableRows = table.findAll('tr')
        films = []
        del tableRows[-2:]
        for index, tr in enumerate(tableRows):
            films.append(index)
            rows = tr.findAll("td")
            for i, info in enumerate(rows):
                if i==1 or i==3:
                    films.append(info.text)
                    # write a row to the csv file
            films.append(genre)
            if index !=0:
                writer.writerow(films)
            films = []

        # close the file
    f.close()


# In[135]:


# genre = ["Adventure", "Comedy", "Drama", "Action", "Thriller-or-Suspense", "Romantic-Comedy"]
# for g in genre:
#     scrapMoviesByGenre(g)

def scrapeReleaseDate(title):
    try:
        site = "https://en.wikipedia.org/wiki/" + title
        print(site)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        page = urlopen(req)
        page_soup = BeautifulSoup(page, "html.parser")
        page.close()
        table = page_soup.find("table", {"class": "infobox vevent"})
        tableRows = table.findAll("tr")
        releaseDate = tableRows[12].findAll('li')
        print(releaseDate[1].text)

        return releaseDate
    except:
        print("no release date found!!")
        return 0
# In[ ]:




