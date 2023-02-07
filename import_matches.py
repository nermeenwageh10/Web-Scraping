import requests
from bs4 import BeautifulSoup
import csv

date=input("please enter a date in the following format  MM/DD/YYYY :")

page=requests.get(f"https://www.yallakora.com/match-center/?date={date}")

def main(page):
    src=page.content
    soup=BeautifulSoup(src,"lxml")
    matches_Details=[]
    
    champions=soup.find_all("div",{"class":"matchCard"})
    def get_all_data(champions):
        champions_title=champions.contents[1].find("h2").text.strip()
        champions_allmatches=champions.contents[3].find_all("li")
        numbers=len(champions_allmatches)
        
        for i in range(numbers):
            teamA=champions_allmatches[i].find("div",{"class":"teamA"}).text.strip()
            teamB=champions_allmatches[i].find("div",{"class":"teamB"}).text.strip()
            
            match_result=champions_allmatches[i].find("div",{"class":"MResult"}).find_all("span")
            score= f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
            
            match_time=champions_allmatches[i].find("div",{"class":"MResult"}).find("span",{"class":"time"}).text.strip()
            matches_Details.append({"نوع البطولة":champions_title,"الفريق الاول":teamA,"الفريق الثاني":teamB,"ميعاد المبارة":match_time,"النتيجة":score})
    for i in range(len(champions)):        
        get_all_data(champions[i])
    keys=matches_Details[0].keys()
    
    with open("matches_details.csv","w",encoding='utf-8') as f:
         dict_writer=csv.DictWriter(f,keys)
         dict_writer.writeheader()
         dict_writer.writerows(matches_Details)
         print("file created")
main(page)
