import pandas as pd
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver

class Oferta():
    
    def __init__(self, div = None, pagina : int = None) -> None:
        
        if div is not None:
            dict_div = get_info(div)
            self.pagina = pagina
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

    def to_df(self) -> pd.DataFrame:
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
                'envio']
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
                'envio':[self.envio]
            })
    
def get_info(div) -> dict:
    
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
        'envio':None
        }
    # Get the inner divs of the main div
    # div is the main div containing the offer information
    inner_divs = div.find_all('div', recursive=False)
    if inner_divs:
        # Tipo de Oferta y Marca
        # inner_divs[1] is the div containing the offer type and brand
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
        # Descripción
        # inner_divs[1] is the div containing the description
        a_elements = inner_divs[1].find_all('a', recursive=False)
        if a_elements:
            dict_output['descripcion'] = a_elements[0].get_text()
        
        div_elements = inner_divs[1].find_all('div', recursive=False)
        if div_elements:
            # Calificación
            # div_elements[0] is the div containing the rating
            span_elements = div_elements[0].find_all('span', recursive=False)
            if span_elements:
                for span_element in span_elements[0]:
                    span_text = span_element.get_text().strip()
                    if span_text:
                        dict_output['calificacion'] = span_text
            # Precio regular
            # div_elements[1] is the div containing the regular price
            s_elements = div_elements[1].find_all('s', recursive=False)
            if s_elements:
                span_elements = s_elements[0].find_all('span', recursive=False)
                precio_regular = ""
                for span_element in span_elements:
                    span_text = span_element.get_text().strip()
                    if len(span_text):
                        precio_regular += span_text
                dict_output['precio_regular'] = precio_regular
            # Precio oferta y descuento
            # div_elements[1] is the div containing the offer price and discount
            div_elements_inner = div_elements[1].find_all('div', recursive=False)
            if div_elements_inner:
                span_elements = div_elements_inner[0].find_all('span', recursive=False)
                if span_elements:
                    dict_output['precio_oferta'] = span_elements[0].get_text()
                if len(span_elements) >=2:
                    dict_output['descuento'] = span_elements[1].text
            # Cuotas, cupon y envio
            # div_elements[1] is the div containing the payment options    
            span_elements = div_elements[1].find_all('span', recursive=False)
            if span_elements:
                for span_element in span_elements:
                    dict_output['cuotas'] = span_element.get_text()
            if len(div_elements)>=3:
                dict_output['cupon'] = div_elements[2].get_text().strip()
            if len(div_elements)>=4:
                dict_output['envio'] = div_elements[3].get_text().strip()
                
    return dict_output       

                
        
        
        # print(div_elements[0])
        # if div_elements:
        #     for div_element in div_elements:
        #         span_elements = div_element.find_all('span', recursive=False)
        #         if span_elements:
        #             for span_element in span_elements:
        #                 print(span_element.text)
            
    
