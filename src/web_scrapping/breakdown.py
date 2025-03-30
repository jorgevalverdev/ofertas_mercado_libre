"""
Breakdown Module

This module defines the `Oferta` class, which is used to process and
structure individual offers scraped from the Mercado Libre website.
"""

import pandas as pd
from bs4.element import Tag


class Oferta:
    """
    Represents an offer scraped from the Mercado Libre website.

    Attributes:
        precio_oferta (float): The price of the offer.
        titulo (str): The title of the offer.
        url (str): The URL of the offer.
        
    Methods:
    
        __init__(self, div: Tag = None, page_number: int = None):
            Initializes an Oferta instance.
        _parse_div(self, div: Tag) -> dict:
            Parses the HTML div element to extract offer details.
        to_df(self) -> pd.DataFrame:
            Converts the offer details into a pandas DataFrame.
    """

    def __init__(self, div : Tag = None, page_number : int = None) -> None:
        """
        Initializes an Oferta instance.

        Args:
            div (BeautifulSoup element): The HTML element containing the
                offer details.
            page_number (int): The page number where the offer was found.
        """
        if div is not None:
            dict_div = self._parse_div(div)
            self.pagina = page_number
            self.tipo_oferta = dict_div['tipo_oferta']
            self.marca = dict_div['marca']
            self.vendedor = dict_div['vendedor']
            self.descripcion = dict_div['descripcion']
            self.calificacion = dict_div['calificacion']
            self.precio_regular = dict_div['precio_regular']
            self.precio_oferta = dict_div['precio_oferta']
            self.descuento = dict_div['descuento']
            self.cuotas = dict_div['cuotas']
            self.cupon = dict_div['cupon']
            self.envio = dict_div['envio']
            self.variaciones = dict_div['variaciones']
        else:
            self.pagina = None
            self.tipo_oferta = None
            self.marca = None
            self.vendedor = None
            self.descripcion = None
            self.calificacion = None
            self.precio_regular = None
            self.precio_oferta = None
            self.descuento = None
            self.cuotas = None
            self.cupon = None
            self.envio = None
            self.variaciones = None

    def _parse_div(self, div : Tag) -> dict:
        """
        Parses the HTML div element to extract offer details.

        Args:
            div (BeautifulSoup element): The HTML element containing the
                offer details.
            page_number (int): The page number where the offer was found.
            
        Returns:
            dict: A dictionary containing the offer details.
        """
        dict_output = {
        'tipo_oferta':None,
        'marca':None,
        'vendedor':None,
        'descripcion':None,
        'calificacion':None,
        'precio_regular':None,
        'precio_oferta':None,
        'descuento':None,
        'cuotas':None,
        'cupon':None,
        'envio':None,
        'variaciones':None
        }
        # Get the inner divs of the main div
        # div is the main div containing the offer information
        inner_divs = div.find_all('div', recursive=False)
        if inner_divs:
            # Tipo de Oferta y Marca
            span_elements = inner_divs[1].find_all('span', recursive=False)
            if span_elements:
                for span_element in span_elements:
                    clase = span_element.get('class')[0]
                    if 'highlight' in clase:
                        dict_output['tipo_oferta'] = span_element.text
                    elif 'brand'in clase:
                        dict_output['marca'] = span_element.text
                    elif 'seller'in clase:
                        dict_output['vendedor'] = span_element.text
                    elif 'variations-text' in clase:
                        dict_output['variaciones'] = span_element.text
                        
            # Descripción
            a_elements = inner_divs[1].find_all('a', recursive=False)
            if a_elements:
                dict_output['descripcion'] = a_elements[0].get_text()
            
            div_elements = inner_divs[1].find_all('div', recursive=False)
            if div_elements:
                for div_element in div_elements:
                    # Calificación
                    if div_element.get('class')[0] == 'poly-component__reviews':
                        dict_output['calificacion'] = div_element.get_text()
                    
                    # Precio regular, precio oferta, descuento y cuotas
                    elif div_element.get('class')[0] == 'poly-component__price':
                        # Precio regular
                        s_elements = div_element.find_all('s', recursive=False)
                        if s_elements:
                            span_elements = s_elements[0].find_all('span', recursive=False)
                            precio_regular = ""
                            for span_element in span_elements:
                                span_text = span_element.get_text().strip()
                                if len(span_text):
                                    precio_regular += span_text
                            dict_output['precio_regular'] = precio_regular
                        
                        # Precio oferta y descuento 
                        div_elements_inner = div_element.find_all('div', recursive=False)
                        if div_elements_inner:
                            span_elements = div_elements_inner[0].find_all('span', recursive=False)
                            if span_elements:
                                dict_output['precio_oferta'] = span_elements[0].get_text()
                            if len(span_elements) >=2:
                                dict_output['descuento'] = span_elements[1].text

                        # Cuotas
                        span_elements = div_element.find_all('span', recursive=False)
                        if span_elements:
                            for span_element in span_elements:
                                dict_output['cuotas'] = span_element.get_text()

                    # Cupón
                    elif div_element.get('class')[0] == 'poly-component__coupons':  
                        dict_output['cupon'] = div_element.get_text().strip()
                    
                    # Envío
                    elif div_element.get('class')[0] == 'poly-component__shipping':  
                        dict_output['envio'] = div_element.get_text().strip()    
          
        return dict_output  

    def to_df(self) -> pd.DataFrame:
        """
        Converts the offer details into a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame containing the offer details.
        """
        if self.descripcion is None:
            columns = [
                'pagina',
                'tipo_oferta', 
                'marca', 
                'vendedor', 
                'descripcion', 
                'calificacion', 
                'precio_regular', 
                'precio_oferta', 
                'descuento', 
                'cuotas', 
                'cupon', 
                'envio',
                'variaciones'
                ]
            return pd.DataFrame(columns=columns)
        else:
            return pd.DataFrame({
                'pagina':[self.pagina],
                'tipo_oferta':[self.tipo_oferta],
                'marca':[self.marca],
                'vendedor':[self.vendedor],
                'descripcion':[self.descripcion],
                'calificacion':[self.calificacion],
                'precio_regular':[self.precio_regular],
                'precio_oferta':[self.precio_oferta],
                'descuento':[self.descuento],
                'cuotas':[self.cuotas],
                'cupon':[self.cupon],
                'envio':[self.envio],
                'variaciones':[self.variaciones]
            })


