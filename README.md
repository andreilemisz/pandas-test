Programa desenhado para fazer uma consulta GET da API específica da discadora 3C+, que retorna um documento JSON com 77 linhas de informação para cada ligação.
O programa transforma esse JSON em um arquivo CSV, com cabeçalhos, e faz três filtragens: última ligação para o número específico, lista com números bons e lista com números ruins.
A ordem de execução das funções é customizável e as variáveis globais estão estabelecidas no começo do programa para que possam ser alteradas com facilidade.

Ordem de funcionamento do programa:
  - O programa começa executando a função "extracao_dados_api" que faz a consulta direto na API da 3C+ e retorna o JSON com as informações solicitadas
  - O segundo passo é a função "arquivo_json_para_csv" que faz a conversão do JSON, cheio de linhas, para um CSV apenas com as colunas que queremos
  - A última função é chamada "execucao_filtragem_relatorio" que começa o processo de leitura, limpeza e emissão dos três relatórios específicos, usando 4 sub-funções
    - A função "relatorio_ultima_ligacao" faz o primeiro relatório
    - Depois a função "substituicao_nome" troca os nomes da planilha para numeros bons e numeros ruins, que será usado nas próximas etapas
    - Por fim, as funções "relatorio_numeros_bons" e "relatorio_numeros_ruins" usam os dados da planilha com os nomes alterados para emitir dois arquivos com os resultados
   
O resultado final completo do programa é a emissão de 1 JSON e 4 CSV.
