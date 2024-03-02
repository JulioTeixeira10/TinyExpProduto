import requests, sys, json, os, error_pop_up
from configparser import ConfigParser


os.makedirs("C:\\TinyProdUni\\", exist_ok=True)

def errorTreatment(dataResponse, mensagem): # Função para tratamento de erro
    codErro = int(dataResponse)
    error_pop_up.log_erro(error_codes[codErro])
    error_pop_up.pop_up_erro(f"{mensagem} {error_codes[codErro]}")
    sys.exit()

def sendRequest(chave, valor, url): # Função para enviar request
    data = f"token={token}&{chave}={valor}&formato=JSON"
    response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    resposta = response.text
    return resposta
    
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

# Importação de dados dos arquivos de configuração
dirToken = "C:\\TinyAPI\\token.cfg"
dirProd = "C:\\TinyProdUni\\dadosProd.cfg"

try:
    # Objeto Token
    configObject1 = ConfigParser()
    configObject1.read(dirToken)
    key = configObject1["KEY"]
    token = key["token"]

    # Objeto Produto
    configObject2 = ConfigParser()
    configObject2.read(dirProd)
    prodData = configObject2["PRODDATA"]
    updtOrIncl = prodData["updtOrIncl"]
    prodCod = prodData["prodCod"]
    prodNome = prodData["prodNome"]
    prodPreco = prodData["prodPreco"]
    prodNCM = prodData["prodNCM"]
    prodQuantidade = prodData["prodQuantidade"]
except Exception as error:
    error_pop_up.log_erro(error)
    error_pop_up.pop_up_erro("Houve um erro no programa, leia o log para mais informações.")
    sys.exit()

# Json com os dados do produto à ser atualizado
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

urlIncProd = 'https://api.tiny.com.br/api2/produto.incluir.php' # Url para incluir produto
urlUpdProd = "https://api.tiny.com.br/api2/produto.alterar.php" # Url para atualizar produto
urlIdProd = "https://api.tiny.com.br/api2/produtos.pesquisa.php" # Url para obter id do produto
urlEstoqProd = "https://api.tiny.com.br/api2/produto.atualizar.estoque.php" # Url para dar entrada ou saída de estoque

if updtOrIncl == "0":
    resposta = sendRequest("produto", produto, urlIncProd)
    dataResponse = json.loads(resposta)
    status = dataResponse["retorno"]["status_processamento"]

    if status == "3": # Solicitação processada corretamente
        error_pop_up.log_info(f"O produto {prodCod} - {prodNome} foi cadastrado com sucesso.")
        error_pop_up.pop_up_check("Produto cadastrado com sucesso.")
        sys.exit()
    elif status == "2": # Solicitação processada, mas possui erros de validação
        errorTreatment(dataResponse["retorno"]["registros"][0]["registro"]["codigo_erro"], "Houve um erro ao cadastrar o produto:")  
    elif status == 1: # Solicitação processada corretamente
        errorTreatment(dataResponse["retorno"]["codigo_erro"], "Houve um erro ao cadastrar o produto:")

elif updtOrIncl == "1":
    resposta = sendRequest("produto", produto, urlUpdProd)
    dataResponse = json.loads(resposta)
    status = dataResponse["retorno"]["status_processamento"]

    if status == "3":
        error_pop_up.log_info(f"O produto {prodCod} - {prodNome} foi atualizado com sucesso.")
        error_pop_up.pop_up_check("Produto atualizado com sucesso.")
        sys.exit()
    elif status == "2":
        errorTreatment(dataResponse["retorno"]["registros"][0]["registro"]["codigo_erro"], "Houve um erro ao atualizar o produto:")
    elif status == 1:
        errorTreatment(dataResponse["retorno"]["codigo_erro"], "Houve um erro ao atualizar o produto:")

elif updtOrIncl == "2":
    resposta = sendRequest("pesquisa", prodCod, urlIdProd)
    dataResponse = json.loads(resposta)
    status = dataResponse["retorno"]["status_processamento"]
    
    if status == "3":
        try:
            id = dataResponse["retorno"]["produtos"][0]["produto"]["id"]
        except Exception as E:
            error_pop_up.log_erro(E)
            error_pop_up.pop_up_erro(f"Houve um erro ao buscar o ID do produto: {E}")
            sys.exit() 
        
        estoque = f'''
                <estoque>
                    <idProduto>{int(id)}</idProduto>
                    <tipo>E</tipo>
                    <quantidade>{float(prodQuantidade)}</quantidade>
                    <observacoes>Lançamento feito através da integração TinyERP-BancaMais.</observacoes>
                </estoque>'''

        resposta = sendRequest("estoque", estoque, urlEstoqProd)

        if status == "3": 
            error_pop_up.log_info(f"Entrada de {prodQuantidade} unidades realizada no produto {prodNome}.")
            error_pop_up.pop_up_check("Entrada de estoque realizada com sucesso.")
            sys.exit()
        elif status == "2": 
            errorTreatment(dataResponse["retorno"]["registros"][0]["registro"]["codigo_erro"], "Houve um erro ao dar entrada no produto:") 
        elif status == 1:
            errorTreatment(dataResponse["retorno"]["codigo_erro"], "Houve um erro ao dar entrada no produto:")

    elif status == "2": 
        errorTreatment(dataResponse["retorno"]["registros"][0]["registro"]["codigo_erro"], "Houve um erro ao pegar o ID do produto:") 
    elif status == 1:
        errorTreatment(dataResponse["retorno"]["codigo_erro"], "Houve um erro ao pegar o ID do produto:")

elif updtOrIncl == "3":
    resposta = sendRequest("pesquisa", prodCod, urlIdProd)
    dataResponse = json.loads(resposta)
    status = dataResponse["retorno"]["status_processamento"]

    if status == "3":
        try:
            id = dataResponse["retorno"]["produtos"][0]["produto"]["id"]
        except Exception as E:
            error_pop_up.log_erro(E)
            error_pop_up.pop_up_erro(f"Houve um erro ao buscar o ID do produto: {E}")
            sys.exit() 
        
        estoque = f'''
                <estoque>
                    <idProduto>{int(id)}</idProduto>
                    <tipo>S</tipo>
                    <quantidade>{float(prodQuantidade)}</quantidade>
                    <observacoes>Lançamento feito através da integração TinyERP-BancaMais.</observacoes>
                </estoque>'''

        resposta = sendRequest("estoque", estoque, urlEstoqProd)

        if status == "3": 
            error_pop_up.log_info(f"Retirada de {prodQuantidade} unidades realizada no produto {prodNome}.")
            error_pop_up.pop_up_check("Retirada de estoque realizada com sucesso.")
            sys.exit()
        elif status == "2":
            errorTreatment(dataResponse["retorno"]["registros"][0]["registro"]["codigo_erro"], "Houve um erro ao fazer a retirada de estoque do produto:")
        elif status == 1:
            errorTreatment(dataResponse["retorno"]["codigo_erro"], "Houve um erro ao fazer a retirada de estoque do produto:")

    elif status == "2":
        errorTreatment(dataResponse["retorno"]["registros"][0]["registro"]["codigo_erro"], "Houve um erro ao pegar o ID do produto:") 
    elif status == 1:
        errorTreatment(dataResponse["retorno"]["codigo_erro"], "Houve um erro ao pegar o ID do produto:")