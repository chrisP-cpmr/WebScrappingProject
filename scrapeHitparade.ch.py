# ! pip3 install requests beautifulsoup4 lxml
# ! pip3 list

# 2021-05, Christoph Meier, https://github.com/chrisP-cpmr
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# For this program the following libraries are used
import requests                                     # Used to request the url and retrieve the html of the site
from bs4 import BeautifulSoup as bs                 # Used to structure the html file and retrieve the needed data
import time                                         # Used to implement a delay when running the program
from datetime import datetime, date, timedelta      # Used to get all Sundays as date which are part of the url

# This function is used to retrieve all Sundays of a specific year, Sunday is when the charts are published
def allsundays(year):
    d = date(year, 1, 1)                    # Get January first
    d += timedelta(days=6 - d.weekday())    # Get the first Sunday of the year
    while d.year == year:                   # As long as the date still corresponds to the initial year run the loop
        yield d.strftime('%d-%m-%Y')        # Return the date in the format needed for the url dd-mm-yyyy
        d += timedelta(days=7)              # Add seven days to the current date to find next Sunday

# This function iterates over every weekly charts from a defined year until the last Sunday from when the script is run
def scrappeHitparade():
    today = datetime.today()                # get the first Sunday of the current year to complete base url
    year = today.year                       # get today's year which will be used to get all Sunday's form the actual year
    actualYearSun = list(allsundays(year))  # get all Sunday's of the actual year
    firstSunday = actualYearSun[0]          # get first Sunday of the actual year, this is needed to construct the initial url

    url = "https://hitparade.ch/charts/singles/" + firstSunday  # constructing the initial url to retrieve the html

    # create user agent for chromium on linux
    user_agent = (
        'Mozilla/5.0 (X11; Linux x86_64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/90.0.4430.93 Safari/537.36'
    )

    # create header
    headers = {'User-Agent': user_agent}

    # grab web page content
    # with request.get() we will get the complete html content of the webpage we are calling
    html = requests.get(url, headers=headers)

    # convert to a beautiful soup object in order to use all functions of BeautifulSoup
    page_soup = bs(html.content, "lxml")

    since = int(input("Since when (year) do you want to scrappe the data? "))   # User can define since when to scape
    weeks = []                          # creating an empty list for all the weeks which will be scraped
    years = list(range(since, year))    # create the range which will be scraped

    # With this loop, all Sunday's in the predefined range, except for the actual year, are recorded
    for year in years:                      # loop through the list of years
        for d in allsundays(year):          # call the function which will generate the list of all Sunday's for one year
            weeks.append(d)                 # append each Sunday to the list 'weeks'

    # this section adds the additional Sunday's of the actual year to the list 'weeks'
    selector = page_soup.find("div", class_="chart_selector_table_cell")    # grab a certain part of the html
    weekSelector = selector.find("select")                                  # grab all the entries for the current weeks
    for week in weekSelector.find_all("option"):                            # loop through every entry
        weeks.append(week.getText().replace(".", "-"))                      # add every entry and adjust format

    # create time for delay and
    delay = 10

    # create file and open the file
    filename = "chartsPyCharm_v2.csv"
    f = open(filename, "w")

    # create and write headers
    fileHeaders = "VW, ArtistAndTitle, WeeksAndRank, Week\n"
    f.write(fileHeaders)

    # count and lastWeek are only used to provide the user with some sort of information about the output of the program
    count = 0               # will be increased by one for every loop
    lastWeek = 'string'     # will provide the last week scraped as a check

    # this loop gets the chart items for every week of the list 'weeks'
    for week in weeks:
        url = "https://hitparade.ch/charts/singles/" + week     # create the url for every specific week
        html = requests.get(url, headers=headers)               # request the html file
        page_soup = bs(html.content, "lxml")                    # convert the html to a BeautifulSoup element
        # once the html is retrieved, we need to find the list of chart items on extract the needed information
        for chartItem in page_soup.find_all("div", class_="content chartitem"):     # get the list of chart items
            VW = chartItem.find("div", class_="chart_lw notmobile").getText().strip()   # retrieve the value for VM
            ArtistAndTitle = chartItem.find("div", class_="chart_title").getText().strip()  # retrive the value for ArtistAndTitle
            WeeksAndRank = chartItem.find("span", class_="wp").getText().strip()    # retrieve the value for WeeksAndRank
            # we have to replace all comas in artist names or titles to ensure no wrong spacing in the .csv
            f.write(VW + "," + ArtistAndTitle.replace(",", "|") + "," + WeeksAndRank + "," + week + "\n")
        time.sleep(delay)   # add a delay to comply with the website constraints
        count += 1          # increase count by 1
        lastWeek = week     # record last week
        break

    # Once everything is scraped, close the file and print some information about the program result
    f.close()
    print("Run successful")
    print('Scraped ' + str(count) + ' times')
    print('Last week scrapped ' + lastWeek)

if __name__ == "__main__":
    scrappeHitparade()
