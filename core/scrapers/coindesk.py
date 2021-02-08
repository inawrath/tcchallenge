import http
import requests

from bs4 import BeautifulSoup
from enum import Enum
from requests import get
from requests.models import Response
from typing import Dict


class CoindeskDataEnum(Enum):
    price: str = 'price'
    metrics: str = 'metrics'
    metrics_return: str = 'metrics_return'


class CoindeskScraper:
    params: dict = {
        'price': {
            'type': CoindeskDataEnum.price,
        },
        'low_24h': {
            'type': CoindeskDataEnum.metrics,
            'search': '24 hour low',
            'classname': 'price-medium',
        },
        'high_24h':{
            'type': CoindeskDataEnum.metrics,
            'search': '24 hour high',
            'classname': 'price-medium',
        },
        'volatility':{
            'type': CoindeskDataEnum.metrics,
            'search': 'volatility (30d)',
            'classname': 'price-medium',
        },
        'returns_24h':{
            'type': CoindeskDataEnum.metrics,
            'search': 'returns (24h)',
            'classname': 'percent-value-text'
        },
        'returns_ytd':{
            'type': CoindeskDataEnum.metrics,
            'search': 'returns (ytd)',
            'classname': 'percent-value-text'
        },
    }

    def __init__(self, url: str) -> None:
        self.url: str = url
        self.__get_html()
        self.__parse_html()
        self.__get_data()

    def __get_html(self) -> None:
        try:
            request: Response = get(self.url)

            if request.status_code != http.HTTPStatus.OK:
                raise Exception(
                    'No se pudo obtener la informacion del scraper. '
                    f'(url: {self.url} - status: {request.status_code})'
                )

        except requests.exceptions.Timeout:
            raise Exception(f'La solicitud a excedido el tiempo maximo. (url: {self.url})')
        except requests.exceptions.ConnectionError:
            raise Exception(f'Problemas al intentar conectarse a (url: {self.url})')

        self.html: str = request.text

    def __parse_html(self) -> None:
        self.soup: BeautifulSoup = BeautifulSoup(self.html, 'html.parser')
        del self.html

    def __get_data(self) -> None:
        for key, value in self.params.items():
            call_function = self.__get_metrics
            
            params = { **value }
            type: str = params['type']
            del params['type']

            if type == CoindeskDataEnum.price:
                call_function = self.__get_price

            params: Dict[str, str] = {
                'key': key,
                **params,
            }

            call_function(**params)

    def __get_price(self, key: str) -> None:
        setattr(self, key, self.__parse_soup_value_to_float(self.soup.find(class_='price-large')))

    def __get_metrics(self, key: str, search: str, classname: str) -> None:
        setattr(
            self,
            key,
            self.__parse_soup_value_to_float(
                self.soup.find(
                    string=lambda s: s.lower() == search,
                ).find_parent(class_='coin-info-block').find(class_=classname),
            ),
        )

    def __parse_soup_value_to_float(self, value) -> float:
        return float(value.text.replace('$', '').replace(',', ''))

    def get_detail(self) -> dict:
        return {
            key: getattr(self, key)
            for key in self.params.keys()
        }
