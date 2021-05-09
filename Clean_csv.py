# 2021-05, Christoph Meier, https://github.com/chrisP-cpmr
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import the needed libraries
import pandas as pd


# create a function to clean the given file
def cleanCsv(filename):
    # read the file with pandas
    weeklyCharts = pd.read_csv(filename,
                          encoding='UTF-8',
                          parse_dates=[' Week'])
    # Create needed columns and copy content
    weeklyCharts['Artist'] = weeklyCharts[' ArtistAndTitle']
    weeklyCharts['Title'] = weeklyCharts[' ArtistAndTitle']
    weeklyCharts['Week(s) in Charts'] = weeklyCharts[' WeeksAndPeak']
    weeklyCharts['Peak'] = weeklyCharts[' WeeksAndPeak']
    weeklyCharts['Rank'] = weeklyCharts[' Rank']
    # delete unneeded columns
    del weeklyCharts[' ArtistAndTitle']
    del weeklyCharts[' WeeksAndPeak']
    del weeklyCharts[' Rank']
    # split the content of the columns and save only needed part for columns "Week(s) in Charts" and "Peak"
    weeklyCharts["Week(s) in Charts"] = weeklyCharts["Week(s) in Charts"].map(lambda n: str(n).split("|")[0])
    weeklyCharts["Peak"] = weeklyCharts["Peak"].map(lambda n: str(n).split("|")[1])
    # remove unneeded strings for columns "Week(s) in Charts" and "Peak"
    weeklyCharts["Week(s) in Charts"] = weeklyCharts["Week(s) in Charts"].str.replace('W ', '', regex=True)
    weeklyCharts["Peak"] = weeklyCharts["Peak"].str.replace('P ', '', regex=True)
    # remove unneeded strings and rename other for column "VW"
    weeklyCharts["VW"] = weeklyCharts["VW"].str.replace('VW ', '', regex=True)
    weeklyCharts["VW"] = weeklyCharts["VW"].str.replace('neu', 'New', regex=True)
    weeklyCharts["VW"] = weeklyCharts["VW"].str.replace('re', 'Return', regex=True)
    # rename the header of the column "VM"
    weeklyCharts.rename(columns={"VW": "PW"}, inplace=False)
    # split the string and save only needed content for "Artist" and "Title"
    weeklyCharts["Artist"] = weeklyCharts["Artist"].map(lambda n: str(n).split("<br/>")[0])
    weeklyCharts["Artist"] = weeklyCharts["Artist"].str.replace('</b>', '', regex=True)
    weeklyCharts["Title"] = weeklyCharts["Title"].map(lambda n: str(n).split("<br/>")[1])
    weeklyCharts["Title"] = weeklyCharts["Title"].str.replace('</a>', '', regex=True)


    weeklyCharts.to_csv("Hitparade.ch_2010_src_stage.csv", index=False)
    print("File has been cleaned and saved!")

if __name__ == "__main__":
    cleanCsv("Hitparade.ch_2010_src_dirty.csv")


