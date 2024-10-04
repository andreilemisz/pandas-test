import json
import csv

# Caminho do arquivo JSON de entrada e do arquivo CSV de saída
input_file = 'json_original.json'  # Altere para o caminho do seu arquivo JSON
output_file = 'output.csv'  # Altere para o caminho do seu arquivo CSV

# Abrir e ler o arquivo JSON
with open(input_file, 'r') as f:
    data = json.load(f)

# Extrair a lista "data" do JSON
data_list = data.get('data', [])

# Abrir o arquivo CSV para escrita
with open(output_file, 'w', newline='') as csvfile:
    # Definir o cabeçalho do CSV
    fieldnames = ['number', 'campaign_id','qualification', "readable_status_text", "mode"]

    # Criar o writer do CSV
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Escrever o cabeçalho no arquivo CSV
    writer.writeheader()
    
    # Escrever os valores de "number" no CSV
    for item in data_list:
        # Obter os valores de "number" e "qualification"
        number_value = item.get('number', None)
        campaign_id_value = item.get('campaign_id', None)
        qualification_value = item.get('qualification', None)
        readable_status_text_value = item.get('readable_status_text', None)
        mode_value = item.get('mode', None)

        ['number', 'campaign_id','qualification', "readable_status_text", "mode"]
        
        if number_value is not None and campaign_id_value is not None and qualification_value is not None and readable_status_text_value is not None and mode_value is not None:
            # Escrever a linha no CSV
            writer.writerow({'number': number_value, 'campaign_id': campaign_id_value, 'qualification': qualification_value, 'readable_status_text': readable_status_text_value, 'mode': mode_value})

print(f"Arquivo CSV foi salvo como {output_file}")