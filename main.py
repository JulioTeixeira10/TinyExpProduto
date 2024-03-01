import requests, sys, json, os, error_pop_up
from configparser import ConfigParser


# Cria o diretório se não existir
os.makedirs("C:\\TinyProdUni\\", exist_ok=True)

dirToken = "C:\\TinyAPI\\token.cfg"
dirProd = "C:\\TinyProdUni\\dadosProd.cfg"

# Dicionário contendo os possiveis erros
error_codes = {
    1: "Token não informado",
    2: "Token inválido ou não encontrado",
    3: "XML mal formado ou com erros",
    4: "Erro de processamento de XML",
    5: "API bloqueada ou sem acesso",
    6: "API bloqueada momentaneamente - muitos acessos no último minuto",
    7: "Espaço da empresa esgotado",
    8: "Empresa bloqueada",
    9: "Números de sequência em duplicidade",
    10: "Parâmetro não informado",
    11: "API bloqueada momentaneamente - muitos acessos concorrentes",
    20: "A Consulta não retornou registros",
    21: "A Consulta retornou muitos registros",
    22: "O XML tem mais registros que o permitido por lote de envio",
    23: "A página que você está tentando obter não existe",
    30: "Erro de Duplicidade de Registro, o produto já está cadastrado no sistema",
    31: "Erros de Validação",
    32: "Registro não localizado",
    33: "Registro localizado em duplicidade",
    34: "Nota Fiscal não autorizada",
    35: "Ocorreu um erro inesperado, tente novamente mais tarde",
    99: "Sistema em manutenção"
}

# Importação de dados
try:
    configObject1 = ConfigParser()
    configObject1.read(dirToken)
    key = configObject1["KEY"]
    token = key["token"]
    configObject2 = ConfigParser()
    configObject2.read(dirProd)
    prodData = configObject2["PRODDATA"]
    updtOrIncl = prodData["updtOrIncl"]
    prodCod = prodData["prodCod"]
    prodNome= prodData["prodNome"]
    prodPreco = prodData["prodPreco"]
    prodNCM = prodData["prodNCM"]
except Exception as error:
    error_pop_up.log_erro(error)
    error_pop_up.pop_up_erro("Houve um erro no programa, leia o log para mais informações.")
    sys.exit()

# Url para incluir produto
urlIncProd = 'https://api.tiny.com.br/api2/produto.incluir.php'

# Url para atualizar produto
urlUpdProd = "https://api.tiny.com.br/api2/produto.alterar.php"

if updtOrIncl == "0":
    # Json com os dados do produto a ser incluido
    produto = f'''{{
        "produtos": [
            {{
                "produto": {{
                    "sequencia": 1,
                    "nome": "{str(prodNome)}",
                    "codigo": "{str(prodCod)}",
                    "unidade": "Un",
                    "preco": {float(prodPreco)},
                    "ncm": "{str(prodNCM)}",
                    "origem": "0",
                    "situacao": "A",
                    "tipo": "P"
                }}
            }}
        ]
    }}'''

    # Request
    data = f"token={token}&produto={produto}&formato=JSON"
    response = requests.post(urlIncProd, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    resposta = response.text

    # Tratamento de erro
    dataResponse = json.loads(resposta)
    status = dataResponse["retorno"]["status_processamento"]

    if status == "3": # Solicitação processada corretamente
        error_pop_up.log_info(f"O produto {prodCod} - {prodNome} foi cadastrado com sucesso.")
        error_pop_up.pop_up_check("Produto cadastrado com sucesso.")
        sys.exit()

    elif status == "2": # Solicitação processada, mas possui erros de validação
        codErro = int(dataResponse["retorno"]["registros"][0]["registro"]["codigo_erro"])
        error_pop_up.log_erro(error_codes[codErro])
        error_pop_up.pop_up_erro(f"Houve um erro ao cadastrar o produto: {error_codes[codErro]}")
        sys.exit()    

    elif status == 1: # Solicitação processada corretamente
        codErro = int(dataResponse["retorno"]["codigo_erro"])
        error_pop_up.log_erro(error_codes[codErro])
        error_pop_up.pop_up_erro(f"Houve um erro ao cadastrar o produto: {error_codes[codErro]}")
        sys.exit()

elif updtOrIncl == "1":
    # Json com os dados do produto a ser incluido
    produto = f'''{{
        "produtos": [
            {{
                "produto": {{
                    "sequencia": 1,
                    "nome": "{str(prodNome)}",
                    "codigo": "{str(prodCod)}",
                    "unidade": "Un",
                    "preco": {float(prodPreco)},
                    "ncm": "{str(prodNCM)}",
                    "origem": "0",
                    "situacao": "A",
                    "tipo": "P"
                }}
            }}
        ]
    }}'''

    # Request
    data = f"token={token}&produto={produto}&formato=JSON"
    response = requests.post(urlUpdProd, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    resposta = response.text

    # Tratamento de erro
    dataResponse = json.loads(resposta)
    status = dataResponse["retorno"]["status_processamento"]

    if status == "3": # Solicitação processada corretamente
        error_pop_up.log_info(f"O produto {prodCod} - {prodNome} foi atualizado com sucesso.")
        error_pop_up.pop_up_check("Produto atualizado com sucesso.")
        sys.exit()

    elif status == "2": # Solicitação processada, mas possui erros de validação
        codErro = int(dataResponse["retorno"]["registros"][0]["registro"]["codigo_erro"])
        error_pop_up.log_erro(error_codes[codErro])
        error_pop_up.pop_up_erro(f"Houve um erro ao atualizar o produto: {error_codes[codErro]}")
        sys.exit()    

    elif status == 1: # Solicitação processada corretamente
        codErro = int(dataResponse["retorno"]["codigo_erro"])
        error_pop_up.log_erro(error_codes[codErro])
        error_pop_up.pop_up_erro(f"Houve um erro ao atualizar o produto: {error_codes[codErro]}")
        sys.exit()