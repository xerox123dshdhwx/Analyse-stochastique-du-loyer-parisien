from fichierjson import *




if __name__ == "__main__":

    # We get from the file all the differente price for each district and for each year and store it in a dict
    avgPriceParisHousing = priceParisHousing("logement-encadrement-des-loyers.json")

    # We get the dict and make the average price for each quarter and for each year
    averagePriceQuarter(avgPriceParisHousing)

    avgMobile = mobileAvg(avgPriceParisHousing)
    # We create a courb that render the 4 avg price of the district for the 4 past years (2019-2020-2021-2022)
    creatingCourbs(avgPriceParisHousing, avgMobile)
    #with the analyse of the precendent courbs we render you the best distrcit the invest in paris
    plt.hist(bestHosingToInvest(avgMobile)[0])
    plt.show()
    #We also show you the best 5 district to invest !
    best5HousingToInvest(avgPriceParisHousing)
    #Render the courbs of the 5 best disctrict to invest in paris
    creatingCourbsFilter(avgPriceParisHousing, avgMobile, coefKeyfiltred)
