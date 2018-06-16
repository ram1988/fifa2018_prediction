
from bs4 import BeautifulSoup
import requests
import pickle

r  = requests.get("https://www.fifa.com/fifa-world-ranking/associations/index.html")
data = r.text
soup = BeautifulSoup(data)
mydivs = soup.find("div", {"class": "ranking-teamlist"})
team_links = []
links = mydivs.find_all("a")

country_history_rankings = {}
for link in links:
    print(link)
    country_name = link.find("img").get("alt")
    r  = requests.get("https://www.fifa.com"+link.get("href"))
    data = r.text
    soup = BeautifulSoup(data)
    ranking_table = soup.find_all("table",{"class":"table tbl-ranking table-striped"})
    ranking_table = ranking_table[1]
    ranks = ranking_table.find_all("td",{"class":"tbl-rank"})
    years = ranking_table.select("td.tbl-deliveryyear > span")
    match_played = ranking_table.select("td.tbl-matchplayed > span")
    wins = ranking_table.select("td.tbl-matchplayed-win > span") 
    
    match_pl = {}
    for i,y in enumerate(years):
      y = y.get_text()
      mp = int(match_played[i].get_text())
      win = int(wins[i].get_text())
      if y not in match_pl:
         match_pl[y] = {"mp":mp,"win":win}
      else:
         obj = match_pl[y]
         obj["mp"] = obj["mp"]+mp
         obj["win"] = obj["win"]+win
      
    rank_year = {}
    for i in range(0,len(ranks)):
        rank = ranks[i].find("span").get_text()
        year = years[i].get_text()
        rank_year[year] = rank
    
    country_history_rankings[country_name] = {"rankings":rank_year,"wins":match_pl}
    
pickle.dump(country_history_rankings,open("fifa_rankings_history.pkl","wb"))
print(country_history_rankings)

