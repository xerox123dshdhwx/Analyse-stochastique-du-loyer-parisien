# Python program to demonstrate
# Conversion of JSON data to
# dictionary

# importing the module
import statistics
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import random

listCoefDirecteur = []
listCoefDirecteurWithKey = []
coefKeyfiltred = []
max = [-1, 0]

def auto_cov(data, n):
    mean = sum(data)/len(data)
    autocov = []
    for h in range(len(data)):
        sigma = []
        for t in range(1, n - h):
            sigma.append((data[t+h] - mean) * (data[t] - mean))
        autocov.append((1/n) * sum(sigma))
    return autocov

def estim_ar2(auto_cor):
    elt = np.array([[auto_cor[0], auto_cor[1]], [auto_cor[1], auto_cor[0]]])
    r = -np.array([auto_cor[1], auto_cor[2]])
    return np.dot(np.linalg.inv(elt), r)

def predict(data, coeff):
    predict_sig = [0 for i in range(len(data))]
    for k in range(1, len(data)-3):
        predict_sig[k + 1] = random.gauss(0, 1) - coeff[0] * predict_sig[k] - coeff[1] * predict_sig[k - 1]
    return predict_sig


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

    global key
    key = list(priceDistrictYear["2019"].keys())
    return priceDistrictYear


def averagePriceQuarter(priceDistrictYear: dict) -> None:
    """
    Modify the dictionary in parameters.
    The function retrieves the list of all prices for a district and averages them
    :param priceDistrictYear:
    :return: None. The parameter is modified by reference.
    """
    for year in (priceDistrictYear):
        x = 0
        for district in (priceDistrictYear[year]):
            x += 1
            moyenne = statistics.mean(priceDistrictYear[year][district])
            priceDistrictYear[year][district] = moyenne


def creatingCourbs(dict: dict, moyenneMobile: dict):
    """
    Displays the average price of a neighbourhood over the last 4 years with the average mobile and the estimation with  autoregressive model
    :param dict:
    :return: Display with matplotlib
    """

    x_point, y_point = np.array([2019, 2020, 2021, 2022]), []
    for k in tqdm(range(50, len(key))):#We plot only the 30 last courbs
        for years in dict:
            y_point.append(dict[years][key[k]])
        x, signal = np.linspace(2019, 2022, 4), np.array(y_point)
        auto_cov_sig = auto_cov(signal, len(signal))
        auto_cor_sig = [auto_cov_sig[k] / auto_cov_sig[0] for k in range(len(auto_cov_sig))]

        coeff = estim_ar2(auto_cor_sig)
        predict_sig = predict(signal, coeff)

        # plt.plot(x, signal, label='Ref. Signal')
        plt.subplot(1, 2, 2)
        plt.plot(x, predict_sig, label='Predict Signals')
        plt.legend(loc=1)
        plt.subplot(1, 2, 1)
        plt.plot(x_point, np.array(y_point), marker='D')
        plt.plot(np.array([2020, 2021]), np.array(moyenneMobile[str(key[k])]), color='r', marker='D')
        plt.ylabel(f'{key[k]}')
        plt.xlabel("Years")
        plt.show()
        y_point = []


def creatingCourbsFilter(dict: dict, moyenneMobile: dict, coefDiMax: list):
    """
    Displays the average price of a neighbourhood over the last 4 years
    :param dict:
    :return: Display with matplotlib
    """
    x_point, y_point = np.array([2019, 2020, 2021, 2022]), []
    for k in range(0, len(coefDiMax)):
        for years in dict:
            y_point.append(dict[years][coefDiMax[k]])
        plt.plot(x_point, np.array(y_point), marker='D')
        plt.ylabel(f'District {coefDiMax[k]}')
        plt.xlabel("Years")
        plt.plot(np.array([2020, 2021]), np.array(moyenneMobile[str(coefDiMax[k])]), color='r', marker='D')
        plt.show()
        y_point = []


def listOfHousing(avgPriceParisHousing: dict) -> list:
    """
    Function that create
    :param avgPriceParisHousing:
    :return:
    """
    y_point, res = [], []
    for districtNumber in range(0, len(key)):
        for years in avgPriceParisHousing:
            y_point.append(avgPriceParisHousing[years][key[districtNumber]])
        res.append((key[districtNumber], y_point))
        y_point = []
    return res


def mobileAvg(avgPriceParisHousing: dict) -> dict:
    """
    Function that create the moving average of the price paris housing data
    :param avgPriceParisHousing:
    :return:
    """
    resF, temp = {}, []
    for k in range(len(key)):
        res = listOfHousing(avgPriceParisHousing)[k][1]
        for indice_dep in range(1, len(res) - 1):
            moyenne = (res[indice_dep] + res[indice_dep - 1] + res[indice_dep + 1]) / 3
            temp.append(moyenne)
        resF.update({key[k]: temp})
        temp = []
    return resF


def coefficient_directeur(double: list):
    y = double
    x = [2020, 2021]
    return (y[1] - y[0]) / (x[1] - x[0])



def bestHosingToInvest(moyenneMobile):
    for k in moyenneMobile:
        coefDirecAvgMobile = coefficient_directeur(moyenneMobile[k])
        listCoefDirecteurWithKey.append([k, coefDirecAvgMobile])
        listCoefDirecteur.append(coefDirecAvgMobile)
        if (coefDirecAvgMobile > max[0]):
            max[0] = coefDirecAvgMobile
            max[1] = k
    print(f'{max[1]} est le meilleur quartier avec un coef de {max[0]}')
    print(
        f'https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/map/?disjunctive.annee&disjunctive.id_zone&disjunctive.nom_quartier&disjunctive.piece&disjunctive.epoque&disjunctive.meuble_txt&sort=nom_quartier&refine.id_quartier={max[1]}&location=12,48.85331,2.30387&basemap=jawg.streets')
    return [listCoefDirecteur, listCoefDirecteurWithKey]




def filtrage(listOfSlopeWithKey: list):
    """
    We look at all the slope of all the moving average courbs and just take those who are superior to 0.5
    :param listOfSlopeWithKey:
    :return:
    """
    for coef in listOfSlopeWithKey:
        if coef[1] > 0.5:
            coefKeyfiltred.append(coef[0])


def best5HousingToInvest(avgPriceParisHousing):
    filtrage(listCoefDirecteurWithKey)
    path = ""
    for districtNumber in list(avgPriceParisHousing["2019"].keys()):
        if (not (districtNumber in coefKeyfiltred)):
            path += f"&exclude.id_quartier={districtNumber}"
    print(f'Voici les 5 quartier les plus prometteur de paris !')
    print(
        f'https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/map/?disjunctive.annee&disjunctive.id_zone&disjunctive.nom_quartier&disjunctive.piece&disjunctive.epoque&disjunctive.meuble_txt&sort=nom_quartier{path}&location=12,48.85331,2.30387&basemap=jawg.streets')