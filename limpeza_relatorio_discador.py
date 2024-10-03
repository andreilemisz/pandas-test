import pandas as pd
import requests
import json
import csv

###########################
# Precisa adicionar a extração do relatório pela API e verificar qual o nome dos cabeçalhos para substituir nas configurações abaixo
###########################

""" Variáveis globais. Alterar para funcionar com o relatório emitido pela API """
# Primeiro as variáveis da API
API_URL = "https://3c.fluxoti.com/api/v1/calls/"
API_Token = "Wg4MWjTAHx0Cy6dZ0Q7rbI6q3i9TTRVtQ84QQGJmfy06A6GUYeLQJSFn802L"
API_ID_Campanha = 142763
API_Dados = {
    "campaigns": [API_ID_Campanha],
    }
API_Headers = {
    "Authorization": f'Bearer {API_Token}'
}

# Depois variáveis sobre a filtragem dos dados
caminho_arquivo = r'C:\Users\conta\Desktop\pasta_padrao_VS_Code\Codigo_Filtro_Discador\Relatorio_Final_Regime.Geral_PR_2025.csv' # Caso o relatório esteja em .csv e não puxado direto da API
cabecalho_data = "DATA_LIGACAO"
cabecalho_qualificacao = "QUALIFICACAO"
cabecalho_telefone = "NUMERO_TELEFONE"
nomes_para_substituir_positivos = ['Retornar depois (contato correto)', 'Não aceitou proposta e sabe da antecipação', 'Não aceitou proposta e NÃO sabe da antecipação', 'Aceitou proposta e sabe da antecipação', 'Aceitou proposta e NÃO sabe da antecipação ', 'Já vendeu', 'Falecido']
nomes_para_substituir_negativos = ['Número errado', 'Não qualificada', 'Mudo', 'Discar novamente', 'Contato de parente e NÃO conseguiu o contato certo', 'Contato de parente e conseguiu o contato certo', 'Caixa Postal', 'Sem qualificação', '-']
nome_positivo = "número_bom"
nome_negativo = "número_ruim"
arquivo_relatorio_ultima_ligacao = "planilha_ultima_ligacao.csv"
arquivo_relatorio_numberos_bons = "planilha_numeros_bons.csv"
arquivo_relatorio_numberos_ruins = "planilha_numberos_ruins.csv"

def extracao_dados_api(API_ID_Campanha):
    """ Apenas ativar essa função se precisar extrair o .csv direto da API da discadora """
    resultado_extracao = requests.get(API_URL, headers=API_Headers, data=json.dumps(API_Dados))
    df_extracao = pd.DataFrame(resultado_extracao)
    df_extracao.to_csv(caminho_arquivo, index=False)

def execucao_filtragem_relatorio(caminho_arquivo):
    """ Passo a Passo das Funções que Serão Executadas """

    # Leitura do csv e alteração da coluna data para entender como datetime (já vem certo)
    df = pd.read_csv(caminho_arquivo)
    df[cabecalho_data] = pd.to_datetime(df[cabecalho_data])

    # Esse relatório não retorna nada para a função, apenas emite a .csv
    relatorio_ultima_ligacao(df)
    # A substituição dos nomes retorna uma nova df já com os valores novos
    substituicao_nomes(df)
    relatorio_numeros_bons(df)
    relatorio_numeros_ruins(df)
    # Fim dos programa. Os 3 .cvs devem estar na pasta geral

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
if __name__ == "__main__":
    extracao_dados_api(API_ID_Campanha)
    execucao_filtragem_relatorio(caminho_arquivo)