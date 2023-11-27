from woocommerce import API
import config
from connection import Connection

wcapi = API(
    url=config.base_url,
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    version="wc/v3"
)

def get_products():
    conn = Connection(config.db)
    ids = []
    try:
        conn.connect()
        query = "SELECT CDPRODUTO, VLUNITARIO FROM TBLVPITEMTABELAPRECO where DTALTERACAO >= DATE('now')"
        products = conn.execute_query(query)
        if len(products) < 1:
            return 0
        for product in products:
            try:
                response = wcapi.get(f'products?sku={product[0]}')
                if response.status_code == 200:
                    data = response.json()
                    ids.append((data[0]['id'],product[1]))
            except Exception as e:
                pass        
    except Exception as e:
        print(e)
    conn.close_connection()

    return ids

def update_products():

    try:

        products = get_products()
        if products == 0:
            return print("Nenhum produto para atualizar")
        for product in products:
            try:
                data = {
                    "regular_price": str(product[1])
                }
                response = wcapi.put(f'products/{product[0]}',data)
                if response.status_code == 200:
                    print(f'Produto {product[0]} Atualizado')
                else:
                    print(response.status_code)
            except Exception as e:
                print(e)
            
    except Exception as e:
        print(e)
while True:
    print('---Atualização de produtos----')
    option = input('1 - Para Atualizar \n2 - Para Sair \nEscolha: ')
    match(option):
        case '1':
            update_products()
            print('Processo finalizado com sucesso')
            break
        case '2':
            print('Sistema finalizado...')
            break
        case _:
            print('Opção inválida')