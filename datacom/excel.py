import re
import pandas as pd
from datetime import timedelta
import os
import sys
# Adiciona o diretório raiz do projeto ao sys.path
RAIZ_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(RAIZ_PROJETO)

# Agora importa o módulo paths
from paths import *

def processar_arquivo_equipment_down():
    dados = []
    linhas_unicas = set()  # Conjunto para armazenar linhas únicas
    
    # Abra o arquivo de log
    with open(caminho_equipment_down_log, 'r') as file:
        linhas = file.readlines()

    for linha in linhas:
        # Verifique se a linha contém "ERROR" seguido do formato desejado
        match = re.search(r"ERROR - Erro: (\d+/\d+/\d+)\s+(\d+)\s+([A-Z0-9]+)\s+(Down)\s+None\s+(.+)", linha)
        if match:
            # Extraia os dados com grupos nomeados
            gpon = match.group(1)
            onu = match.group(2)
            serial_number = match.group(3)
            oper_state = match.group(4)
            name = match.group(5).strip()  # Remova espaços em branco extras

            # Crie uma tupla para evitar duplicatas
            linha_tupla = (gpon, onu, serial_number, oper_state, name)
            
            if linha_tupla not in linhas_unicas:
                dados.append([gpon, onu, serial_number, oper_state, name])
                linhas_unicas.add(linha_tupla)

    # Crie um DataFrame com os dados únicos
    df = pd.DataFrame(dados, columns=['GPON', 'ONU', 'Serial Number', 'Oper State', 'Name'])

    # Salve o DataFrame em um arquivo Excel
    df.to_excel(caminho_equipment_down_xlsx, index=False)

def processar_arquivo_down_time():

    dados_onus = []
    outros_nomes = []

    # Regex para capturar as informações específicas
    regex = {
        "ID": r"ID\s+:\s+(\d+)",
        "Serial Number": r"Serial Number\s+:\s+(\w+)",
        "Last Seen Online": r"Last Seen Online\s+:\s+([\d\w\s,:]+)",
        "Name": r"Name\s+:\s+([\w_]+)",
        "Operational state": r"Operational state\s+:\s+(\w+)"
    }

    # Abrindo o arquivo de log e processando linha a linha
    with open(caminho_down_time_log, 'r') as file:
        bloco_atual = {}
        for linha in file:
            # Checando cada campo relevante
            for campo, padrao in regex.items():
                match = re.search(padrao, linha)
                if match:
                    bloco_atual[campo] = match.group(1)
            
            # Condição para salvar o bloco atual (quando o bloco estiver completo)
            if "Operational state" in bloco_atual:
                # Verificar se o Last Seen Online é maior ou igual a 90 dias
                last_seen = bloco_atual.get("Last Seen Online", "")
                dias_match = re.search(r"(\d+)\s+days", last_seen)
                dias = int(dias_match.group(1)) if dias_match else 0

                if dias >= 90:
                    # Verificar se o nome contém uma das palavras-chave
                    nome = bloco_atual.get("Name", "").lower()
                    if any(termo in nome for termo in ["EMPRESA A", "EMPRESA B", "EMPRESA C"]): #Esse campo e adicionado para identificar nome das ONUs das empresas parceiras para não serem removidas
                        outros_nomes.append(bloco_atual)
                    else:
                        dados_onus.append(bloco_atual)
                    
                bloco_atual = {}  # Reiniciar o bloco

    # Criando os DataFrames
    df_onus = pd.DataFrame(dados_onus)
    df_outros_nomes = pd.DataFrame(outros_nomes)

    # Salvando em Excel
    df_onus.to_excel(caminho_Clientes_time_down_xlsx, index=False)
    df_outros_nomes.to_excel(caminho_Clientes_time_down_outras_empresas_xlsx, index=False)

    print("Dados salvos com sucesso!")

def processar_service_port():
    # Lista para armazenar os resultados
    dados = []
    
    # Expressão regular para capturar service-port, gpon e onu
    padrao = r"service-port (\d+) gpon (\S+) onu (\d+)"
    
    # Abrir e ler o arquivo de log
    with open(caminho_service_port_log, 'r') as f:
        for linha in f:
            # Procurar pelo padrão nas linhas
            match = re.search(padrao, linha)
            if match:
                # Adicionar os dados encontrados à lista
                service_port = match.group(1)
                gpon = match.group(2)
                onu = match.group(3)
                dados.append([service_port, gpon, onu])
    
    # Criar um DataFrame a partir dos dados extraídos
    df = pd.DataFrame(dados, columns=['Service-Port', 'GPON', 'ONU'])
    
    # Salvar o DataFrame no arquivo Excel
    df.to_excel(caminho_service_port_xlsx, index=False)
    
    print("Dados extraídos e salvos com sucesso!")

def verificar_arquivo(caminho):
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}. Certifique-se de que o arquivo existe.")
        return False
    return True

def processar_dos_arquivos_excel():
    # Verificar existência dos arquivos
    if not verificar_arquivo(caminho_Clientes_time_down_xlsx) or \
       not verificar_arquivo(caminho_equipment_down_xlsx) or \
       not verificar_arquivo(caminho_service_port_xlsx):
        exit(1)
    
    # Carregar as planilhas
    planilha1 = pd.read_excel(caminho_Clientes_time_down_xlsx)
    planilha2 = pd.read_excel(caminho_equipment_down_xlsx)
    planilha3 = pd.read_excel(caminho_service_port_xlsx)
    
    # Verificar colunas necessárias
    if 'Serial Number' not in planilha1.columns or 'Serial Number' not in planilha2.columns:
        print("A coluna 'Serial Number' está ausente em uma das planilhas.")
        exit(1)
    
    # Realizar o primeiro merge
    resultado = pd.merge(planilha1, planilha2, on='Serial Number', how='inner')

    if 'GPON' not in resultado.columns or 'ONU' not in resultado.columns:
        print("As colunas 'GPON' e/ou 'ONU' estão ausentes.")
        exit(1)

    # Realizar o segundo merge
    resultado_final = pd.merge(resultado, planilha3, on=['GPON', 'ONU'], how='inner')

    # Remover colunas desnecessárias
    colunas_remover = ['Oper State', 'Name_y', 'ID']
    colunas_existentes = [col for col in colunas_remover if col in resultado_final.columns]
    resultado_final = resultado_final.drop(columns=colunas_existentes)

    # Remover duplicatas
    resultado_final = resultado_final.drop_duplicates()

    # Salvar o resultado final
    resultado_final.to_excel(caminho_resultado_processar_dos_arquivos_excel_xlsx, index=False)
    print(f"Resultado salvo em: {caminho_resultado_processar_dos_arquivos_excel_xlsx}")

