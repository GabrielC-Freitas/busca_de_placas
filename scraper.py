import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.pichau.com.br/hardware/placa-de-video?page={}"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

nomes_e_precos_placas = {}

# Iterar sobre as páginas
for page_num in range(1, 64):
    url = base_url.format(page_num)
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    
    # Encontrar os elementos que contêm os nomes e preços das placas de vídeo
    placas = soup.find_all('h2', class_=lambda x: x and 'MuiTypography-h6' in x)
    precos = soup.find_all('div', class_='jss1290')

    # Extrair os nomes e preços das placas de vídeo e adicioná-los ao dicionário
    for placa, preco in zip(placas, precos):
        nome = placa.text.strip()
        preco = preco.text.strip() if preco else "Preço não disponível"
        print(f"Nome: {nome}, Preço: {preco}")  # Print adicionado para depuração
        nomes_e_precos_placas[nome] = preco

# Criar arquivo CSV com os nomes e preços das placas de vídeo
with open('placas_de_video.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Nome', 'Preço'])
    for nome, preco in nomes_e_precos_placas.items():
        csv_writer.writerow([nome, preco])
