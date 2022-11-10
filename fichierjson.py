# Python program to demonstrate
# Conversion of JSON data to
# dictionary

# importing the module
import statistics
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


def priceParisHousing(fileName: str) -> dict:
    """
    A function that organizes the data with all the prices of all the districts of Paris and for the year (2019-2020-2021-2022).
    :param: fileName: Json file of paris housing price
    return: dict
    """

    # We read en extract the data from the json file
    with open(fileName) as json_file:
        data = json.load(json_file)

    priceDistrictYear = {
        "2019": {},
        "2020": {},
        "2021": {},
        "2022": {},
    }

    for k in tqdm(range(len(data))):
        price = data[k]['fields']['ref']
        Year = data[k]['fields']['annee']
        district = str(data[k]['fields']['id_quartier'])
        value = priceDistrictYear[Year].setdefault(district)
        if (value):
            x = priceDistrictYear[Year][district]
            x.append(price)
        else:
            priceDistrictYear[Year].update({district: [price]})
    return priceDistrictYear


def averagePriceQuarter(priceDistrictYear: dict) -> None:
    """
    Modify the dictionary in parameters.
    The function retrieves the list of all prices for a district and averages them
    :param priceDistrictYear:
    :return: None. The parameter is modified by reference.
    """
    for year in tqdm(priceDistrictYear):
        x = 0
        for district in tqdm(priceDistrictYear[year]):
            x += 1
            moyenne = statistics.mean(priceDistrictYear[year][district])
            priceDistrictYear[year][district] = moyenne


def creatingCourbs(dict: dict, moyenneMobile: dict):
    """
    Displays the average price of a neighbourhood over the last 4 years
    :param dict:
    :return: Display with matplotlib
    """

    x_point, y_point = np.array([2019, 2020, 2021, 2022]), []
    key = list(dict["2019"].keys())
    print(key)
    for k in range(0, len(key)):
        for years in dict:
            y_point.append(dict[years][key[k]])
        plt.plot(x_point, np.array(y_point), marker='D')
        plt.ylabel(f'District {key[k]}')
        plt.xlabel("Years")
        plt.plot(np.array([2020, 2021]), np.array(moyenneMobile[str(key[k])]), color='r', marker='D')
        plt.show()
        y_point = []


def creatingCourbsFilter(dict: dict, moyenneMobile: dict, coefDiMax: list):
    """
    Displays the average price of a neighbourhood over the last 4 years
    :param dict:
    :return: Display with matplotlib
    """

    x_point, y_point = np.array([2019, 2020, 2021, 2022]), []
    key = coefDiMax
    print(key)
    for k in range(0, len(key)):
        for years in dict:
            y_point.append(dict[years][key[k]])
        plt.plot(x_point, np.array(y_point), marker='D')
        plt.ylabel(f'District {key[k]}')
        plt.xlabel("Years")
        plt.plot(np.array([2020, 2021]), np.array(moyenneMobile[str(key[k])]), color='r', marker='D')
        plt.show()
        y_point = []


def listOfHousing(dict: dict) -> list:
    y_point, res = [], []
    key = list(dict["2019"].keys())
    for k in range(0, len(key)):
        for years in dict:
            y_point.append(dict[years][key[k]])
        res.append((key[k], y_point))
        y_point = []
    return res


def mobileAvg(avgPriceParisHousing: dict) -> dict:
    resF, temp = {}, []
    key = list(avgPriceParisHousing["2019"].keys())
    for k in range(len(key)):
        res = listOfHousing(avgPriceParisHousing)[k][1]
        for indice_dep in range(1, len(res) - 1):
            moyenne = (res[indice_dep] + res[indice_dep - 1] + res[indice_dep + 1]) / 3
            temp.append(moyenne)
        print(temp)
        resF.update({key[k]: temp})
        temp = []
    return resF


def coefficient_directeur(double: list):
    y = double
    x = [2020, 2021]
    return (y[1] - y[0]) / (x[1] - x[0])


# We get from the file all the differente price for each district and for each year and store it in a dict
avgPriceParisHousing = priceParisHousing("logement-encadrement-des-loyers.json")

print(avgPriceParisHousing)

# We get the dict and make the average price for each quarter and for each year
averagePriceQuarter(avgPriceParisHousing)

moyenneMobile = mobileAvg(avgPriceParisHousing)
print(moyenneMobile)
# We create a courb that render the 4 avg price of the district for the 4 past years (2019-2020-2021-2022)
creatingCourbs(avgPriceParisHousing, moyenneMobile)
listCoefDirecteur = []
listCoefDirecteurWithKey = []
coefKeyfiltred = []
print(moyenneMobile)
max = [-1, 0]
for k in moyenneMobile:
    res = coefficient_directeur(moyenneMobile[k])
    listCoefDirecteurWithKey.append([k, res])
    listCoefDirecteur.append(res)
    print(f'Distrcit {k} as {res}')
    if (res > max[0]):
        max[0] = res
        max[1] = k
print(f'{max[1]} est le meilleur quartier avec un coef de {max[0]}')
print(
    f'https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/map/?disjunctive.annee&disjunctive.id_zone&disjunctive.nom_quartier&disjunctive.piece&disjunctive.epoque&disjunctive.meuble_txt&sort=nom_quartier&refine.id_quartier={max[1]}&location=12,48.85331,2.30387&basemap=jawg.streets')
print(listCoefDirecteur)
print(listCoefDirecteurWithKey)
plt.hist(listCoefDirecteur)
plt.show()


def filtrage(list: list) -> list:
    res = []
    for coef in list:
        if coef[1] > 0.5:
            res.append(coef)
            coefKeyfiltred.append(coef[0])
    return res


print(filtrage(listCoefDirecteurWithKey))
print(coefKeyfiltred)
path = ""
print(list(avgPriceParisHousing["2019"].keys()))
for key in list(avgPriceParisHousing["2019"].keys()):
    if (not (key in coefKeyfiltred)):
        path += f"&exclude.id_quartier={key}"

print(path)
print(
    f'https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/map/?disjunctive.annee&disjunctive.id_zone&disjunctive.nom_quartier&disjunctive.piece&disjunctive.epoque&disjunctive.meuble_txt&sort=nom_quartier{path}&location=12,48.85331,2.30387&basemap=jawg.streets')

creatingCourbsFilter(avgPriceParisHousing, moyenneMobile, coefKeyfiltred)
