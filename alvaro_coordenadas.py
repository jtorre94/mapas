import logging
from sys import stdout
from typing import Tuple

import pandas as pd
import requests

logging.basicConfig(stream=stdout, level=logging.DEBUG)


def geocoding(
        address: str = None,
        county: str = None,
        city: str = None,
        postcode: str = None
) -> Tuple[float]:
    """ Based on an address, returns its longitude and latitude.

    :param address: input address. It does not need a strict format.
    :type address: str
    :param county: provincia.
    :type county: str
    :param city: ciudad.
    :type city: str
    :param postcode: codigo postal.
    :type postcode: str
    :return: longitude and latitude of the address.
    :rtype: Tuple[float]
    """

    url = 'https://api.geoapify.com/v1/geocode/search'
    params = {
        'text': address,
        'county': county,
        'city': city,
        'postcode': postcode,
        'apiKey': 'b444eca29f2340af8eadb4e7a244c8ee'
    }
    r = requests.get(url, params=params)
    try:
        results = r.json()['features']
        logging.debug(r.json())
        lon, lat = results[0]['geometry']['coordinates']
        return lat, lon
    except IndexError as ie:
        logging.exception(ie)
        return None, None


def return_df_with_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """ Adds 2 columns with longitude and latitude to the input dataframe.

    :param df: input dataframe.
    :type df: pd.DataFrame
    :return: formatted dataframe.
    :rtype: pd.DataFrame
    """

    df = df.copy()
    df['COORDENADAS'] = \
        df.apply(lambda row: geocoding(
            address=row['CALLE'].encode('latin1'),
            city=row['CIUDAD'].encode('latin1'),
            county=row['PROVINCIA'].encode('latin1'),
            postcode=row['CODIGO POSTAL']
        ), axis=1)

    df[['LATITUD', 'LONGITUD']] = pd.DataFrame(df['COORDENADAS'].tolist(), index=df.index)
    df.drop('COORDENADAS', axis=1, inplace=True)
    return df


def main():
    df = pd.read_csv('map_test.csv', encoding='latin1')
    df = return_df_with_coordinates(df)
    df.to_csv('mydata.csv', index=False, encoding='latin1')


if __name__ == '__main__':
    main()
