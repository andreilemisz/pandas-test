import os
import requests
import json
import csv

###########################
# Atenção: 
# Sempre verificar qual o nome dos cabeçalhos para substituir nas configurações abaixo
# Também pode desativar funções específicas no final dependendo se já tiver JSON ou CSV pronto
###########################

""" Variáveis globais. Alterar para funcionar com o relatório emitido pela API """

# Primeiro as variáveis da API
API_URL = "https://app.pipedrive.com/v1/deals"
API_Token = "e37b66824d179873e05068de200c483234c190f1"
API_Dados = {
    "user_id": "22163022",
    "api_token": API_Token,
    "limit": 20
    }

# Caminho onde está o JSON pronto, se for o caso. Não é necessário preencher se for fazer a request da API automaticamente
caminho_json = 'planilha_metas_geral_precs.json' 
# O próximo começa vazio. Vai ser preenchido se fizer a consulta na API ou se fizer o load padrão da execução do programa. Se fizer o load automatico do programa, ele vai puxar o JSON que estiver no caminho da variavel "caminho_json" que está estabelecida acima
dados_em_json = None
# Local onde será criado o arquivo .CSV, que será usado para carregar as funções de filtragem. Se não for fazer a conversão de JSON para CSV e já tiver a tabela pronta, basta alterar o caminho dela aqui
caminho_csv = "planilha_metas_geral_precs.csv"

# Segundo passo, variáveis da transformação do JSON em CSV
# Para novos valores, precisa adicionar nessa variável e dentro da função arquivo_json_para_csv nos dois momentos perto do fim
# Esse lugar é o nome do cabeçalho das colunas, então pode ser renomeado do jeito que quiser, desde que apareca lá no fim vinculado com alguma variável de valor
valores_a_buscar = ["usuario_criador", "usuario_atual", "id_estagio_atual", "numero_processo", "valor", "data_criacao", "data_ultima_atualizacao", "status_atual", "id_do_pipeline", "data_mudanca_estagio", "data_da_vitoria"]

def extracao_dados_api(): 
    """ Apenas ativar essa função se precisar extrair o JSON direto da API da discadora """
    
    # Comando GET para pegar os dados da API
    resultado_extracao = requests.get(API_URL, params=API_Dados)
    dados_em_json = resultado_extracao.json()

    # Criando o arquivo JSON com o que foi extraído da request
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(dados_em_json, f, ensure_ascii=False, indent=4)

    return dados_em_json

    # O fim dessa função é a extração em JSON da consulta na API da discadora
    # O JSON está salvo na variável "dados_em_json" para ser usado nas próximas etapas

def arquivo_json_para_csv(dados_em_json):
    """ Essa função pega o arquivo JSON no argumento 1 (dados_em_json) e transforma ele em um arquivo .CSV com cabeçalho e os valores específicos das linhas que a gente selecionar nas variáveis gerais e no final da função nos campos específicos """
    
    # A categoria 'data' é uma lista dentro do retorno em JSON e é onde estão os valores que a gente precisa, por isso precisa fazer essa busca primeiro
    dados_na_categoria_correta = dados_em_json.get('data', [])
    with open(caminho_csv, 'w', newline="", encoding="utf-8") as arquivocsv:
        cabecalhos = valores_a_buscar
        funcao_escritor = csv.DictWriter(arquivocsv, fieldnames=cabecalhos)
        funcao_escritor.writeheader()

        """ Aqui é preciso escrever cada valor que for puxado para coluna """
        for linha in dados_na_categoria_correta:
            usuario_criador_valor = linha.get('creator_user_id', None).get("name")
            usuario_atual_valor = linha.get('user_id', None).get("name", None)
            id_estagio_atual_valor = linha.get('stage_id', None)
            numero_processo_valor = linha.get("title", None)
            valor_valor = linha.get("value", None)
            data_criacao_valor = linha.get("add_time", None)
            data_ultima_atualizacao_valor = linha.get("update_time", None)
            status_atual_valor = linha.get("status", None)
            id_do_pipeline_valor = linha.get("pipeline_id", None)
            
            # Esses dois valores só funcionam quando tem if/else, porque eles podem ser preenchidos no JSON como "null" e por algum motivo ele buga a planilha inteira se ele identificar esse valor
            if linha.get("stage_change_time") == None:
                data_mudanca_estagio_valor = "Vazio"
            else:
                data_mudanca_estagio_valor = linha.get("stage_change_time", None)

            if linha.get("won_time") == None:
                data_da_vitoria_valor = "Vazio"
            else:
                data_da_vitoria_valor = linha.get("won_time", None)

            # Modelo
                # _valor = linha.get("", None)

            """ Mesma coisa aqui, para cada coluna a ser adicionada tem que adicionar a sintaxe abaixo nos dois lugares """
            if usuario_criador_valor is not None and usuario_atual_valor is not None and id_estagio_atual_valor is not None and numero_processo_valor is not None and valor_valor is not None and data_criacao_valor is not None and data_ultima_atualizacao_valor is not None and status_atual_valor is not None and id_do_pipeline_valor is not None and data_mudanca_estagio_valor is not None and data_da_vitoria_valor is not None:
                funcao_escritor.writerow({'usuario_criador': usuario_criador_valor, 'usuario_atual': usuario_atual_valor, 'id_estagio_atual': id_estagio_atual_valor, 'numero_processo': numero_processo_valor, 'valor': valor_valor, 'data_criacao': data_criacao_valor, 'data_ultima_atualizacao': data_ultima_atualizacao_valor, 'status_atual': status_atual_valor, 'id_do_pipeline': id_do_pipeline_valor,'data_mudanca_estagio': data_mudanca_estagio_valor, 'data_da_vitoria': data_da_vitoria_valor})

    # O fim dessa função é a criação de uma planilha CSV criada com cabeçalhos e os valores que a gente decidiu filtrar

###########################
""" Execução do Programa """
""" Programar quais operações são necessárias, na ordem """

if __name__ == "__main__":

        # O resultado dessa primeira função é que a variavel "dados_em_json" contem a JSON da consulta feita
    if not os.path.exists(caminho_json):
        extracao_dados_api()

        # Para o próximo passo, é preciso que a variável 'dados_em_json' esteja com um arquivo JSON já lido. Isso já está certo se extracao_dados_api() for usado antes. Se não for o caso, ele ativa a leitura do JSON que está na variável "caminho_json" que é configurada no cabeçalho do programa
    if dados_em_json == None:
        with open(caminho_json, 'r', encoding="utf-8") as json_aberto:
            dados_em_json = json.load(json_aberto)

        # Terceiro passo é transformar o arquivo JSON que está em "dados_em_json" para uma tabela CSV
    arquivo_json_para_csv(dados_em_json)

# Fim do programa