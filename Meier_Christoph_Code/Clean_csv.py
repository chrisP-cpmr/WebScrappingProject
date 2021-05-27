# 2021-05, Christoph Meier, https://github.com/chrisP-cpmr
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import the needed libraries
import pandas as pd


# create a function to clean the given file
def cleanCsv(filename):
    # read the file with pandas
    weeklyCharts = pd.read_csv(filename,
                               parse_dates=[' Week'],
                               dayfirst=True)
    # Create needed columns and copy content
    weeklyCharts['Artist'] = weeklyCharts[' ArtistAndTitle']
    weeklyCharts['Title'] = weeklyCharts[' ArtistAndTitle']
    weeklyCharts['Week(s) in Charts'] = weeklyCharts[' WeeksAndPeak']
    weeklyCharts['Peak'] = weeklyCharts[' WeeksAndPeak']
    weeklyCharts['Rank'] = weeklyCharts[' Rank']
    weeklyCharts['Week'] = weeklyCharts[' Week']
    # delete unneeded columns
    del weeklyCharts[' ArtistAndTitle']
    del weeklyCharts[' WeeksAndPeak']
    del weeklyCharts[' Rank']
    del weeklyCharts[' Week']
    # drop rows with the value "200" in "Week(s) in Charts" and "Peak"
    dropListW = weeklyCharts.index.get_indexer_for((weeklyCharts[weeklyCharts["Week(s) in Charts"] == "200"].index))
    weeklyCharts = weeklyCharts.drop(weeklyCharts.index[dropListW])
    dropListP = weeklyCharts.index.get_indexer_for((weeklyCharts[weeklyCharts["Peak"] == "200"].index))
    weeklyCharts = weeklyCharts.drop(weeklyCharts.index[dropListP])
    # split the content of the columns and save only needed part for columns "Week(s) in Charts" and "Peak"
    weeklyCharts["Week(s) in Charts"] = weeklyCharts["Week(s) in Charts"].map(lambda n: str(n).split("|")[0])
    weeklyCharts["Peak"] = weeklyCharts["Peak"].map(lambda n: str(n).split("|")[1])
    # remove unneeded strings for columns "Week(s) in Charts" and "Peak"
    weeklyCharts["Week(s) in Charts"] = weeklyCharts["Week(s) in Charts"].str.replace('W ', '', regex=True)
    weeklyCharts["Peak"] = weeklyCharts["Peak"].str.replace('P ', '', regex=True)
    weeklyCharts["Week(s) in Charts"] = weeklyCharts["Week(s) in Charts"].str.replace(' ', '', regex=True)
    weeklyCharts["Peak"] = weeklyCharts["Peak"].str.replace(' ', '', regex=True)
    # remove unneeded strings and rename other for column "VW"
    weeklyCharts["VW"] = weeklyCharts["VW"].str.replace('VW ', '', regex=True)
    weeklyCharts["VW"] = weeklyCharts["VW"].str.replace('neu', 'New', regex=True)
    weeklyCharts["VW"] = weeklyCharts["VW"].str.replace('re', 'Return', regex=True)
    # rename the header of the column "VM"
    weeklyCharts = weeklyCharts.rename(columns = {'VW': 'PW'}, inplace=False)
    # split the string and save only needed content for "Artist" and "Title" and strip
    weeklyCharts["Artist"] = weeklyCharts["Artist"].map(lambda n: str(n).split("<br/>")[0])
    weeklyCharts["Artist"] = weeklyCharts["Artist"].str.replace('</b>', '', regex=True)
    weeklyCharts["Artist"] = weeklyCharts["Artist"].str.replace('&amp;', '&', regex=True)
    weeklyCharts["Artist"] = weeklyCharts["Artist"].map(lambda n: str(n).strip())
    weeklyCharts["Title"] = weeklyCharts["Title"].map(lambda n: str(n).split("<br/>")[1])
    weeklyCharts["Title"] = weeklyCharts["Title"].str.replace('</a>', '', regex=True)
    weeklyCharts["Artist"] = weeklyCharts["Artist"].str.replace('&amp;', '&', regex=True)
    weeklyCharts["Title"] = weeklyCharts["Title"].map(lambda n: str(n).strip())
    # convert values to int
    weeklyCharts['Week(s) in Charts'] = weeklyCharts['Week(s) in Charts'].astype(int)
    weeklyCharts['Peak'] = weeklyCharts['Peak'].astype(int)
    # sort values
    weeklyCharts = weeklyCharts.sort_values(by=["Artist", "Title", "Week(s) in Charts", "Peak"], ascending = False)
    # remove all duplicates with the subset "Artist" and "Title", this will result in one song being in the list
    # only once and not for every week
    weeklyCharts = weeklyCharts.drop_duplicates(subset=["Artist", "Title"])
    # delete unneeded column "PW"
    del weeklyCharts["PW"]
    del weeklyCharts["Rank"]
    # create a file of the data
    weeklyCharts.to_csv("../Meier_Christoph_Data/Hitparade.ch_2010_stage.csv", index=False)
    print("File has been cleaned and saved!")

if __name__ == "__main__":
    cleanCsv("../Meier_Christoph_Data/Hitparade.ch_2010_src_dirty.csv")


