#!/usr/bin/env python
# coding: utf-8

# In[126]:


from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import csv


# In[127]:


def scrapMoviesByGenre(genre):
    year = ["2015","2016","2017","2018","2019","2020"]
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


# In[ ]:


genre = ["Adventure", "Comedy", "Drama", "Action", "Thriller-or-Suspense", "Romantic-Comedy"]
for g in genre:
    scrapMoviesByGenre(g)


# In[ ]:




