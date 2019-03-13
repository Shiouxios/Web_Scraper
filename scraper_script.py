########### SETUP ###########

from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector

x=200

for i in range (0,30):

    # Create URL, changing for each iteration
    first = 38308
    suffix = first + x

    quote_page = 'https://www.premierleague.com/match/' + str(suffix)
    id = quote_page[36:42]

    page = urlopen(quote_page)
    allPage = BeautifulSoup(page, 'html.parser')

    # Take data from URL

    ### DATE ###
    matchWeekAll = allPage.find("div", class_="current")
    matchWeekLong = matchWeekAll.find("div", class_="short").text
    matchWeek = ''.join(ch for ch in matchWeekLong if ch.isdigit())

    ### TEAMS ###
    homeTeamAll = allPage.find("div", class_="team home")
    homeTeamNorm = homeTeamAll.find("span", class_="long").text
    homeTeam = homeTeamNorm.replace(" ", "")
    homeTeamShort = homeTeam[0:3]

    awayTeamAll = allPage.find("div", class_="team away")
    awayTeamNorm = awayTeamAll.find("span", class_="long").text
    awayTeam = awayTeamNorm.replace(" ", "")
    awayTeamShort = awayTeam[0:3]

    ### SCORE ###
    score = allPage.find("div", class_="score fullTime").text
    scoreHome = score[0]
    scoreAway = score[2]

    ### POINTS ###

    if scoreHome > scoreAway:
        pointsHome = 3
        pointsAway = 0
    elif scoreHome == scoreAway:
        pointsHome = 1
        pointsAway = 1
    else:
        pointsHome = 0
        pointsAway = 3

    #### Goals and Assists ####
    goals = allPage.find("div", class_="matchEvents")

    # Home goals---------------------------------------------
    homeGoalsAll = goals.find("div", class_="home")

    homeGoals = []
    for i in range(0, len(homeGoalsAll.find_all("a"))):
        loop = homeGoalsAll.find_all("a")[i].text
        homeGoals.append(loop)

    #print(homeGoals)

    # Away goals---------------------------------------------
    awayGoalsAll = goals.find("div", class_="away")

    awayGoals = []
    for i in range(0, len(awayGoalsAll.find_all("a"))):
        loop = awayGoalsAll.find_all("a")[i].text
        awayGoals.append(loop)

    #print(awayGoals)

    #### Assists ####

    assists = allPage.find("div", class_="matchAssistsContainer")

    # Home assists---------------------------------------------
    homeAssistsAll = assists.find("div", class_="home")

    homeAssists = []
    for i in range(0, len(homeAssistsAll.find_all("a"))):
        loop = homeAssistsAll.find_all("a")[i].text
        homeAssists.append(loop)

    #print(homeAssists)

    # Away assists---------------------------------------------
    awayAssistsAll = assists.find("div", class_="away")

    awayAssists = []
    for i in range(0, len(awayAssistsAll.find_all("a"))):
        loop = awayAssistsAll.find_all("a")[i].text
        awayAssists.append(loop)

    ### SEND TO SQL ###
    cnx = mysql.connector.connect(user='root', password='XXXXXX',
                                host='localhost',
                                database='prem')

    mycursor = cnx.cursor()

    mycursor.execute("INSERT INTO matches (matchID, matchWeek, homeTeam, awayTeam, homeScore, awayScore, homePoints, awayPoints) \
            \
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (id, matchWeek, homeTeam, awayTeam, scoreHome, scoreAway, pointsHome, pointsAway))

    cnx.commit()
    cnx.close()

    x = x + 1
    print(x, "records inserted.")


