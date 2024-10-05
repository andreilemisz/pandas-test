import os
import pandas as pd
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
API_URL = "https://3c.fluxoti.com/api/v1/calls/"
API_Token = "Wg4MWjTAHx0Cy6dZ0Q7rbI6q3i9TTRVtQ84QQGJmfy06A6GUYeLQJSFn802L"
API_ID_Campanha = 142763
API_Dados = {
    "campaigns": list({API_ID_Campanha}),
    "per_page": 5
    }
API_Headers = {
    "Authorization": f'Bearer {API_Token}'
}

# Caminho onde está o JSON pronto, se for o caso. Não é necessário preencher se for fazer a request da API automaticamente
caminho_json = 'consulta_API_ligacoes.json' 
# O próximo começa vazio. Vai ser preenchido se fizer a consulta na API ou se fizer o load padrão da execução do programa. Se fizer o load automatico do programa, ele vai puxar o JSON que estiver no caminho da variavel "caminho_json" que está estabelecida acima
dados_em_json = None
# Local onde será criado o arquivo .CSV, que será usado para carregar as funções de filtragem. Se não for fazer a conversão de JSON para CSV e já tiver a tabela pronta, basta alterar o caminho dela aqui
caminho_csv = "tabela_dados_discadora.csv"

# Segundo passo, variáveis da transformação do JSON em CSV
# Para novos valores, precisa adicionar nessa variável e dentro da função arquivo_json_para_csv nos dois momentos perto do fim
valores_a_buscar = ['number', 'call_date', 'campaign_id','qualification', "readable_status_text", 'phone_type', "mode"]

# Terceiro, variáveis sobre a filtragem dos dados
cabecalho_data = "call_date"
cabecalho_qualificacao = "qualification"
cabecalho_telefone = "number"
nomes_para_substituir_positivos = ['Retornar depois (contato correto)', 'Não aceitou proposta e sabe da antecipação', 'Não aceitou proposta e NÃO sabe da antecipação', 'Aceitou proposta e sabe da antecipação', 'Aceitou proposta e NÃO sabe da antecipação ', 'Já vendeu', 'Falecido']
nomes_para_substituir_negativos = ['Número errado', 'Não qualificada', 'Mudo', 'Discar novamente', 'Contato de parente e NÃO conseguiu o contato certo', 'Contato de parente e conseguiu o contato certo', 'Caixa Postal', 'Sem qualificação', '-']
nome_positivo = "número_bom"
nome_negativo = "número_ruim"
arquivo_relatorio_ultima_ligacao = "planilha_ultima_ligacao.csv"
arquivo_relatorio_numberos_bons = "planilha_numeros_bons.csv"
arquivo_relatorio_numberos_ruins = "planilha_numberos_ruins.csv"

def extracao_dados_api(): # Com problema, ainda não está trazendo apenas a campanha específica
    """ Apenas ativar essa função se precisar extrair o JSON direto da API da discadora """
    
    # Comando GET para pegar os dados da API
    resultado_extracao = requests.get(API_URL, headers=API_Headers, json=API_Dados)
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
            number_value = linha.get('number', None)
            call_date_value = linha.get('call_date', None)
            campaign_id_value = linha.get('campaign_id', None)
            qualification_value = linha.get('qualification', None)
            readable_status_text_value = linha.get('readable_status_text', None)
            phone_type_value = linha.get('phone_type', None)
            mode_value = linha.get('mode', None)

            """ Mesma coisa aqui, para cada coluna a ser adicionada tem que adicionar a sintaxe abaixo nos dois lugares """
            if number_value is not None and call_date_value is not None and campaign_id_value is not None and qualification_value is not None and readable_status_text_value is not None and phone_type_value is not None and mode_value is not None:

                funcao_escritor.writerow({'number': number_value, 'call_date': call_date_value, 'campaign_id': campaign_id_value, 'qualification': qualification_value, 'readable_status_text': readable_status_text_value, 'phone_type': phone_type_value, 'mode': mode_value})

    # O fim dessa função é a criação de uma planilha CSV criada com cabeçalhos e os valores que a gente decidiu filtrar

def execucao_filtragem_relatorio(caminho_csv):
    """ Passo a Passo das Funções que Serão Executadas para as Filtragens """

    # Leitura do csv e alteração da coluna data para entender como datetime (já vem certo)
    df = pd.read_csv(caminho_csv)
    df[cabecalho_data] = pd.to_datetime(df[cabecalho_data])

    # Esse relatório não retorna nada para a função, apenas emite a .csv
    relatorio_ultima_ligacao(df)
    # A "substituição_nomes" retorna uma nova df já com os valores novos
    substituicao_nomes(df)
    # Relatórios separados, usando a df criada na função acima
    relatorio_numeros_bons(df)
    relatorio_numeros_ruins(df)
    # Fim dos programa. Os 3 .csv devem estar na pasta geral

def relatorio_ultima_ligacao(df):
    """ Usado para calcular quantos telefones únicos foram alimentados na campanha """

    df_ultima_ligacao = df.loc[df.groupby(cabecalho_telefone)[cabecalho_data].idxmax()]
    df_ultima_ligacao.to_csv(arquivo_relatorio_ultima_ligacao, index=False)

def substituicao_nomes(df):
    """ Troca dos nomes das qualificações ruins e boas por 'numero_bom' e 'numero_ruim'. Precisa ser atualizado sempre que uma campanha muda as regras de preenchimento, ou outro termo é adicionado nas qualificações """

    df[cabecalho_qualificacao] = df[cabecalho_qualificacao].replace(nomes_para_substituir_positivos, nome_positivo)
    df[cabecalho_qualificacao] = df[cabecalho_qualificacao].replace(nomes_para_substituir_negativos, nome_negativo)
    return df

def relatorio_numeros_bons(df):
    """ Emissão do relatório em .csv apenas com os números BONS, sem repetir o mesmo telefone """

    df_positivo = df[df[cabecalho_qualificacao] == nome_positivo]
    df_positivo.to_csv(arquivo_relatorio_numberos_bons, index=False)

def relatorio_numeros_ruins(df):
    """ Emissão do relatório em .csv apenas com os números RUINS, sem repetir o mesmo telefone """

    df_negativos = df[df[cabecalho_qualificacao] == nome_negativo]
    df_negativos = df_negativos.loc[df_negativos.groupby(cabecalho_telefone)[cabecalho_data].idxmax()]
    df_negativos.to_csv(arquivo_relatorio_numberos_ruins, index=False)

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

        # Por último, a função vai criar o relatório da última ligação (para ver quantos números não repetidos foram discados), depois vai criar o relatório só com números bons não repetidos, e por fim, relatório de números ruins não repetidos
    execucao_filtragem_relatorio(caminho_csv)

# Fim do programa