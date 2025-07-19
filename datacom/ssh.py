import paramiko
import logging
from time import sleep
import pandas as pd
import datetime as dt
import os
from datetime import datetime

import sys


# Adiciona o diretório raiz do projeto ao sys.path
RAIZ_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(RAIZ_PROJETO)
from paths import *

# Obtém a data e hora atual
agora = datetime.now()

# Exibe a data e hora
print("Data e hora atual:", agora)

# Formatar a data e hora para exibição mais amigável
data_formatada = agora.strftime("%Y-%m-%d_%H-%M-%S")
print("Data e hora formatada:", data_formatada)

hostname1 = 'IP do Jumper'
porta1 = 'porta'
usuario1 = 'usuario'
senha1 = 'senha'

hostname2 = 'IP do Datacom'
usuario2 = 'usuario'
senha2 = 'senha'




# Configuração do logger principal para a conexão (nível INFO)
logger_conexao = logging.getLogger('conexao')
logger_conexao.setLevel(logging.INFO)
handler_conexao = logging.FileHandler(caminho_ssh_execution_log)
handler_conexao.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger_conexao.addHandler(handler_conexao)



def equipment_down(hostname1, porta1, usuario1, senha1, hostname2, usuario2, senha2):

    comando = 'show interface gpon onu | i Down | nomore'
    # Configuração do logger para a execução do comando (nível DEBUG)
    logger_comando = logging.getLogger('comando')
    logger_comando.setLevel(logging.DEBUG)
    handler_comando = logging.FileHandler(caminho_equipment_down_log)
    handler_comando.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger_comando.addHandler(handler_comando)
    
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Conexão ao primeiro host
        cliente.connect(hostname1, port=porta1, username=usuario1, password=senha1)
        logger_conexao.info(f'Conectado ao {hostname1} como {usuario1}')
        
        # Conectando ao segundo host via SSH
        stdin, stdout, stderr = cliente.exec_command(f'ssh -tt {usuario2}@{hostname2}', get_pty=True)
        
        # Espera pela resposta inicial
        sleep(1)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta inicial: {resultado.strip()}')
        
        if 'password:' in resultado.lower():
            stdin.write(senha2 + '\n')
            stdin.flush()
            logger_conexao.info('Senha enviada.')
        
        sleep(1)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta após autenticação: {resultado.strip()}')


        # Parte onde o comando é executado com logging em nível DEBUG
        logger_comando.info(f'Executando comando: {comando}')
        stdin.write(comando + '\n')
        stdin.flush()

        
        saida_comando = ""

        timeout_seconds = 50  # Definindo um tempo limite de 10 segundos
        sleep_interval = 1  # Intervalo para verificar a saída
        start_time = dt.datetime.now()

        while True:
     
 
            if stderr.channel.recv_ready():
                erro = stderr.channel.recv(1024).decode()
                logger_comando.error(f'Erro: {erro.strip()}')

                            # Verifica se o tempo limite foi alcançado
            elapsed_time = (dt.datetime.now() - start_time).total_seconds()
            if elapsed_time > timeout_seconds:
                logger_conexao.error('Tempo limite de execução excedido.')
                retorno = 'Tempo limite de execução excedido.'
                cliente.close()
                break

            if stdout.channel.exit_status_ready():
                break

    except Exception as e:
        logger_conexao.error(f"Erro: {str(e)}")
    
    finally:
        cliente.close()
        logger_conexao.info('Conexão encerrada.')
        return "Sucesso"

def backup_olt_datacom(hostname1, porta1, usuario1, senha1, hostname2, usuario2, senha2):
    comando = 'show running-config | nomore'
    # Configuração do logger para a execução do comando (nível DEBUG)
    logger_comando = logging.getLogger('comando')
    logger_comando.setLevel(logging.DEBUG)
    handler_comando = logging.FileHandler(fr'./applications/equipments/datacom/backup_OLT/olt_datacom_{hostname2}_{agora}_{data_formatada}.log')
    handler_comando.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger_comando.addHandler(handler_comando)
    
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Conexão ao primeiro host
        cliente.connect(hostname1, port=porta1, username=usuario1, password=senha1)
        logger_conexao.info(f'Conectado ao {hostname1} como {usuario1}')
        
        # Conectando ao segundo host via SSH
        stdin, stdout, stderr = cliente.exec_command(f'ssh -tt {usuario2}@{hostname2}', get_pty=True)
        
        # Espera pela resposta inicial
        sleep(1)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta inicial: {resultado.strip()}')
        
        if 'password:' in resultado.lower():
            stdin.write(senha2 + '\n')
            stdin.flush()
            logger_conexao.info('Senha enviada.')
        
        sleep(1)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta após autenticação: {resultado.strip()}')


        # Parte onde o comando é executado com logging em nível DEBUG
        logger_comando.info(f'Executando comando: {comando}')
        stdin.write(comando + '\n')
        stdin.flush()

        
        saida_comando = ""

        timeout_seconds = 50  # Definindo um tempo limite de 10 segundos
        sleep_interval = 1  # Intervalo para verificar a saída
        start_time = dt.datetime.now()

        while True:
     
 
            if stderr.channel.recv_ready():
                erro = stderr.channel.recv(1024).decode()
                logger_comando.error(f'Erro: {erro.strip()}')

                            # Verifica se o tempo limite foi alcançado
            elapsed_time = (dt.datetime.now() - start_time).total_seconds()
            if elapsed_time > timeout_seconds:
                logger_conexao.error('Tempo limite de execução excedido.')
                retorno = 'Tempo limite de execução excedido.'
                cliente.close()
                break

            if stdout.channel.exit_status_ready():
                break

    except Exception as e:
        logger_conexao.error(f"Erro: {str(e)}")
    
    finally:
        cliente.close()
        logger_conexao.info('Conexão encerrada.')
        return "Backup"

def down_time(hostname1, porta1, usuario1, senha1, hostname2, usuario2, senha2):
    logger_comando = logging.getLogger('down_time_comando')  # Nome exclusivo para o logger
    logger_comando.setLevel(logging.DEBUG)
    handler_comando = logging.FileHandler(caminho_down_time_log)
    handler_comando.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger_comando.addHandler(handler_comando)
    
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Conexão ao primeiro host
        cliente.connect(hostname1, port=porta1, username=usuario1, password=senha1)
        logger_conexao.info(f'Conectado ao {hostname1} como {usuario1}')
        
        # Conectando ao segundo host via SSH
        stdin, stdout, stderr = cliente.exec_command(f'ssh -tt {usuario2}@{hostname2}', get_pty=True)
        
        # Espera pela resposta inicial
        sleep(1)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta inicial: {resultado.strip()}')
        
        if 'password:' in resultado.lower():
            stdin.write(senha2 + '\n')
            stdin.flush()
            logger_conexao.info('Senha enviada.')
        
        sleep(2)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta após autenticação: {resultado.strip()}')

        # Carregar o Excel para executar os comandos 
        tabela = pd.read_excel(caminho_equipment_down_xlsx)
        tabela_devedores = tabela.loc[tabela['Oper State']=='Down']
        dados = tabela_devedores[['GPON','ONU','Serial Number','Oper State','Name']].values.tolist()
        total_dados = len(dados)  # Total de itens para verificar o último
        for index, dado in enumerate(dados):
            gpon, onu, serial_number, open_state, name = dado

            # Executar o comando para a ONU específica
            comando = f"show interface gpon {gpon} onu {onu} | nomore"
            logger_comando.info(f'Executando comando: {comando}')
            stdin.write(comando + '\n')
            stdin.flush()
            sleep(1)  # Ajuste o tempo de espera conforme necessário

            # Ler a saída do comando
            if stdout.channel.recv_ready():
                saida = stdout.channel.recv(4096).decode()
                logger_comando.info(f'Saída do comando: {saida.strip()}')

    except Exception as e:
        logger_conexao.error(f"Erro: {str(e)}")
    
    finally:
        cliente.close()
        logger_conexao.info('Conexão encerrada.')
        return "Down_Time"


def service_port(hostname1, porta1, usuario1, senha1, hostname2, usuario2, senha2):
    comando = 'show running-config service-port | nomore'
    # Configuração do logger para a execução do comando (nível DEBUG)
    logger_comando = logging.getLogger('service_port_comando')  # Nome exclusivo para o logger
    logger_comando.setLevel(logging.DEBUG)
    handler_comando = logging.FileHandler(caminho_service_port_log)
    handler_comando.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger_comando.addHandler(handler_comando)
    
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Conexão ao primeiro host
        cliente.connect(hostname1, port=porta1, username=usuario1, password=senha1)
        logger_conexao.info(f'Conectado ao {hostname1} como {usuario1}')
        
        # Conectando ao segundo host via SSH
        stdin, stdout, stderr = cliente.exec_command(f'ssh -tt {usuario2}@{hostname2}', get_pty=True)
        
        # Espera pela resposta inicial
        sleep(1)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta inicial: {resultado.strip()}')
        
        if 'password:' in resultado.lower():
            stdin.write(senha2 + '\n')
            stdin.flush()
            logger_conexao.info('Senha enviada.')
        
        sleep(1)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta após autenticação: {resultado.strip()}')

        # Executar o comando para exibir a configuração do service-port
        logger_comando.info(f'Executando comando: {comando}')
        stdin.write(comando + '\n')
        stdin.flush()

        # Processando a saída do comando
        saida_comando = ""
        timeout_seconds = 50  # Tempo limite de 50 segundos
        sleep_interval = 1  # Intervalo para verificar a saída
        start_time = dt.datetime.now()

        while True:
            if stderr.channel.recv_ready():
                erro = stderr.channel.recv(1024).decode()
                logger_comando.error(f'Erro: {erro.strip()}')
                
            # Verifica se o tempo limite foi alcançado
            elapsed_time = (dt.datetime.now() - start_time).total_seconds()
            if elapsed_time > timeout_seconds:
                logger_conexao.error('Tempo limite de execução excedido.')
                retorno = 'Tempo limite de execução excedido.'
                cliente.close()
                break

            if stdout.channel.exit_status_ready():
                break

            # Coleta a saída do comando, se disponível
            if stdout.channel.recv_ready():
                output = stdout.channel.recv(1024).decode()
                saida_comando += output
                logger_comando.info(f'Parte da saída: {output.strip()}')

        # Verificar se a saída foi coletada corretamente
        if saida_comando:
            logger_comando.info(f'Saída final do comando: {saida_comando.strip()}')
        else:
            logger_comando.warning('Nenhuma saída recebida para o comando de configuração do service-port.')
        
    except Exception as e:
        logger_conexao.error(f"Erro na execução do comando ou na conexão: {str(e)}")
    
    finally:
        cliente.close()
        logger_conexao.info('Conexão encerrada.')
        return "Service_Port"


def delete_onu(hostname1, porta1, usuario1, senha1, hostname2, usuario2, senha2):

    logger_comando = logging.getLogger('comando_delete_onu')
    logger_comando.setLevel(logging.DEBUG)
    handler_comando = logging.FileHandler(caminho_delete_onu_log)
    handler_comando.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger_comando.addHandler(handler_comando)

    # Configuração de conexão SSH
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conectar ao primeiro host
        cliente.connect(hostname1, port=porta1, username=usuario1, password=senha1)
        logger_conexao.info(f'Conectado ao {hostname1} como {usuario1}')
        
        # Conectar ao segundo host via SSH
        stdin, stdout, stderr = cliente.exec_command(f'ssh -tt {usuario2}@{hostname2}', get_pty=True)
        
        # Aguardar resposta inicial e enviar senha se necessário
        sleep(1)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta inicial: {resultado.strip()}')
        
        if 'password:' in resultado.lower():
            stdin.write(senha2 + '\n')
            stdin.flush()
            logger_conexao.info('Senha enviada.')
        
        sleep(2)
        resultado = stdout.channel.recv(1024).decode()
        logger_conexao.info(f'Resposta após autenticação: {resultado.strip()}')

        # Carregar dados do Excel
        tabela = pd.read_excel(caminho_resultado_processar_dos_arquivos_excel_xlsx)

        # Filtrar ONUs que estão "Down"
        tabela_devedores = tabela.loc[tabela['Operational state'] == 'Down']
        
        # Selecionar as colunas necessárias
        dados = tabela_devedores[['Serial Number', 'Last Seen Online', 'Name_x', 'Operational state', 'GPON', 'ONU', 'Service-Port']].values.tolist()

        # Configuração no dispositivo
        stdin.write('config\n')
        stdin.flush()
        sleep(2)

        # Executar os comandos para cada ONU
        for dado in dados:
            serial_number, last_seen_online, name_x, operational_state, gpon, onu, service_port = dado

            # Comandos para excluir a ONU
            comandos = [
                f"no service-port {service_port}",
                f"interface gpon {gpon}",
                f"no onu {onu}",
                "commit",
                "exit"
            ]
            logger_conexao.info(f'Executando comandos para ONU {onu} com GPON {gpon}')
            
            for comando in comandos:
                try:
                    logger_comando.info(f'Executando comando: {comando}')
                    stdin.write(comando + '\n')
                    stdin.flush()
                    sleep(10)  # Ajuste de tempo conforme necessário
                    
                    # Verificar saída do comando
                    saida = ""
                    while stdout.channel.recv_ready():
                        saida += stdout.channel.recv(4096).decode()
                    
                    # Log da saída do comando
                    logger_comando.info(f'Saída do comando: {saida.strip()}')

                    if "Aborted" in saida or "error" in saida.lower():
                        logger_comando.error(f'Erro detectado após o comando: {comando}')
                        sleep(10)
                        break

                except Exception as e:
                    logger_comando.error(f"Erro ao executar comando '{comando}': {str(e)}")
                
    except Exception as e:
        logger_conexao.error(f"Erro de conexão ou execução de comandos: {str(e)}")
    
    finally:
        cliente.close()
        logger_conexao.info('Conexão encerrada.')
        return "Limpeza_onu_finalizada"

def clear_folder():

    # Lista de caminhos das pastas que você quer limpar
    pastas = [r'./Excel', r'./File_Log']

    # Para cada pasta na lista, percorre e apaga todos os arquivos
    for caminho_da_pasta in pastas:
        for arquivo in os.listdir(caminho_da_pasta):
            caminho_arquivo = os.path.join(caminho_da_pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
        print(f"Todos os arquivos na pasta '{caminho_da_pasta}' foram apagados.")

    print("Limpeza completa.")


