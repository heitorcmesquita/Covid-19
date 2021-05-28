import urllib.request
import pandas as pd
import requests
from bs4 import BeautifulSoup
from os import remove

#buscando a página que tem as url's com os csv's dos registros de vacinação
url = 'https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/ef3bd0b8-b605-474b-9ae5-c97390c197a8'
page = requests.get(url)

#fazendo webscrapping para retornar as url's
soup = BeautifulSoup(page.content, 'html.parser')
a = soup.find_all('a', href = True)

#criando lista vazia e colocando as url's dentro dela. Depois, eliminando elementos indesejados da lista
urls = []
for i in a:
    urls.append(i['href'])
urls = urls[14:51]
del(a, page, url)

#criando df vazio, e iniciando iteração para baixar csv's dos estados
base = pd.DataFrame()    
for url in urls:
    try:
        urllib.request.urlretrieve(url, 'vacinadosbuscar.csv')
        
        #lendo csv por chunks e agrupando os vacinados
        for chunk in pd.read_csv('vacinadosbuscar.csv', sep = ';', encoding = 'utf-8', chunksize = 100000):
            chunk['count'] = ''
            chunk = chunk.groupby(['paciente_idade', 'vacina_fabricante_nome', 'vacina_descricao_dose', 'estabelecimento_uf'], as_index = False)['count'].count()
            base = base.append(chunk)
        print(chunk['estabelecimento_uf'][0])
    except:
        print('erro')
        pass

remove('vacinadosbuscar.csv')

#colocando dados em um csv
base.to_csv('vacinados.csv', sep = ';', encoding = 'iso-8859-1', index = False)
