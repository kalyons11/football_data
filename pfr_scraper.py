## Ben Kite
## Forked by Kevin Lyons, updated Dec 2020 and beyond

import pandas
import requests, bs4
import re

class PFRScraper:
    @classmethod
    def find_tables(cls, url):
        """
        Provides a list of the html tables that can be found at the url
        provided.  The order in the list returned should reflect the order
        that the tables appear.  On pro-football-reference.com, these names
        usually indicate what information they contain.
        
        For example:
        PFRScraper.find_tables("http://www.pro-football-reference.com/boxscores/201702050atl.htm")
        """
        res = requests.get(url)
        comm = re.compile("<!--|-->")
        soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
        divs = soup.findAll('div', id = "content")
        divs = divs[0].findAll("div", id=re.compile("^all"))
        ids = []
        for div in divs:
            searchme = str(div.findAll("table"))
            x = searchme[searchme.find("id=") + 3: searchme.find(">")]
            x = x.replace("\"", "")
            if len(x) > 0:
                ids.append(x)
        
        return ids

    
    @classmethod
    def pull_table(cls, url, tableID, header = True):
        """
        Pulls a table (indicated by tableID, which can be identified with
        "find_tables") from the specified url. The header option determines
        if the function should try to determine the column names and put
        them in the returned data frame. The default for header is True.
        If you get an index error for data_header, try specifying header =
        False. I will include a generated error message for that soon.
        
        For example:
        url = "http://www.pro-football-reference.com/boxscores/201702050atl.htm"
        PFRScraper.pull_table(url, "team_stats")
        """
        res = requests.get(url)
        ## Work around comments
        comm = re.compile("<!--|-->")
        soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
        tables = soup.findAll('table', id = tableID)
        data_rows = tables[0].findAll('tr')
        game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
            for i in range(len(data_rows))
            ]
        data = pandas.DataFrame(game_data)
        if header == True:
            data_header = tables[0].findAll('thead')
            data_header = data_header[0].findAll("tr")
            data_header = data_header[0].findAll("th")
            header = []
            for i in range(len(data.columns)):
                header.append(data_header[i].getText())
            data.columns = header
            data = data.loc[data[header[0]] != header[0]]
        data = data.reset_index(drop = True)
        
        return data


    @classmethod
    def find_season_stats(cls, stat, year):
        """
        Finds offensive player data for a given season.
        This one was written with fantasy football GMs in mind.
        stat indicates what statistic is desired.
        the user must specify "passing", "rushing", or "receiving"
        the year indicates the year in which the season of interest started
        seasonFinder("passing", 2016)
        
        For example:
        tables = ["passing", "rushing", "receiving"]
        years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                 2009, 2010, 2011, 2012, 2013, 2014, 2015]
        for y in years:
            for t in tables:
                PFRScraper.find_season_stats(t, y)
        """
        url = "http://www.pro-football-reference.com/years/" + str(year) + "/" + stat + ".htm"
        if stat == "rushing":
            stat = "rushing_and_receiving"
        dat = PFRScraper.pull_table(url, stat, header=False)
        dat = dat.reset_index(drop = True)
        names = dat.columns
        for c in range(0, len(names)):
            replacement = []
            if type (dat.loc[0][c]) == str:
                k = names[c]
                for i in range(0, len(dat[k])):
                    p = dat.loc[i][c]
                    xx = re.sub("[#@*&^%$!+]", "", p)
                    xx = xx.replace("\xa0", "_")
                    xx = xx.replace(" ", "_")
                    replacement.append(xx)
                dat[k] = replacement
        
        return dat


    @classmethod
    def find_play_by_play(cls, date, home_team):
        """
        Finds the play by play table a game with the date and home team provided.
        The date has to be yyyymmdd with a 0 on the end.
        The reference sites use the trailing 0 incase there are multiple games on the same day (it happens in baseball).
        For the 2017 Superbowl the date of February 5th, 2017 would be 201702050.
        The team is the three letter abbrieviation for the home team in lower case.
        
        For example:
        This provides the play by play for the 2017 Superbowl.
        PFRScraper.find_play_by_play("201702050", "atl")
        """
        url = "http://www.pro-football-reference.com/boxscores/" +  str(date) + home_team + ".htm"
        dat = PFRScraper.pull_table(url, "pbp")
        dat = dat.reset_index(drop = True)
        dat = dat.loc[dat["Detail"] != "None"]
        return dat


    @classmethod
    def pull_combine_data(cls, year, pos=None):
        """
        This function provides an easy way to access NFL scouting combine data.
        The year indicates the year the combine was held.
        The pos argument can be used to specify a position to pull data for.
        If pos is not specified all data will be pulled.
        
        For example:
        This pulls all data for Quarterbacks in 2016
        PFRScraper.pull_combine_data(2016, "QB")
        """
        url = "http://www.pro-football-reference.com/draft/" + str(year) + "-combine.htm"
        dat = PFRScraper.pull_table(url, "combine")
        dat["year"] = year
        if pos is not None:
            dat = dat.loc[dat["Pos"] == pos]
        return dat

