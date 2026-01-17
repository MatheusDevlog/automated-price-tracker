import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


PRODUCT_URL = 'https://www.mercadolivre.com.br/notebook-acer-nitro-v15-anv15-52-51e4-intel-core-i5-13420h-de-13g-512gb-ssd-16-gb-ram-rtx4050-156-fhd/p/MLB60407347?pdp_filters=item_id%3AMLB5840007964#origin%3Dshare%26sid%3Dshare%26wid%3DMLB5840007964'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9'
}

TARGET_PRICE =  130.00

def check_price():
    try:
        response = requests.get(PRODUCT_URL, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')

        title_element = soup.find('h1', class_='ui-pdp-title')
        title = title_element.get_text().strip() if title_element else 'Produto sem título'
        
        price_element = soup.find('span', class_='andes-money-amount__fraction')

        if price_element:
            text_value = price_element.get_text().replace(".","")
            current_price = float(text_value)

            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            if current_price <= TARGET_PRICE:
                print (f'[{now}] 🔥 OPORTUNIDADE! {title} baixou para R$: {current_price}')
            else:
                print(f'[{now}] ⏳ {title} custa R$: {current_price}. (Alvo: R$ {TARGET_PRICE})')

            with open('historico_preco.txt', 'a', encoding='utf-8') as file:
                file.write(f'{now} - R$: {current_price}\n')

        else:
            print('❌ Não foi possivel encontrar a TAG de preço no site.')

    except Exception as e:
        print(f'❌ Ocorreu um erro inesperado: {e}')

if __name__ == '__main__':
    print('🚀 Monitor de Preços Iniciado...')

    while True:
        check_price()
        print('Proxima verificação em 1 hora')
        time.sleep(3600)
