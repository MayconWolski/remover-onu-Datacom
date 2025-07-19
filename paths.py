import os


# Diretório principal do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Exemplo de Caminho para os arquivos Excel e .log dos Datacom 
EQUIPMENT_DOWN_LOG = os.path.join(BASE_DIR, 'applications', 'equipments', 'datacom', 'File_Log', 'equipment_down.log')
EQUIPAMENTOS_DOWN_EXCEL = os.path.join(BASE_DIR, 'applications', 'equipments', 'datacom', 'Excel', 'Equipamentos_Down.xlsx')


#Caminho ssh_execution.log e 

caminho_ssh_execution_log = os.path.join(BASE_DIR, 'applications','equipments','datacom','File_Log','ssh_execution.log')

#Caminho do arquivo equipment_down e Equipamentos_Down.xlsx

caminho_equipment_down_log = os.path.join(BASE_DIR, 'applications','equipments','datacom','File_Log','equipment_down.log')
caminho_equipment_down_xlsx = os.path.join(BASE_DIR, 'applications','equipments','datacom','Excel','equipment_down.xlsx')

#Caminho do arquivo down_time.log e down_time.xlsx

caminho_down_time_log = os.path.join(BASE_DIR, 'applications','equipments','datacom','File_Log','down_time.log')


#Caminho do arquivo service_port.log e service_port.xlsx
caminho_service_port_log = os.path.join(BASE_DIR, 'applications','equipments','datacom','File_Log','service_port.log')
caminho_service_port_xlsx = os.path.join(BASE_DIR, 'applications','equipments','datacom','Excel','service_port.xlsx')

#Caminho do arquivo delete_onu_.log

caminho_delete_onu_log = os.path.join(BASE_DIR, 'applications','equipments','datacom','File_Log','delete_onu.log')

#Caminho do Excel resultado_processar_dos_arquivos_excel.xlsx

caminho_resultado_processar_dos_arquivos_excel_xlsx = os.path.join(BASE_DIR, 'applications','equipments','datacom','Excel','resultado_processar_dos_arquivos_excel.xlsx')

caminho_Clientes_time_down_outras_empresas_xlsx = os.path.join(BASE_DIR, 'applications','equipments','datacom','Excel','Clientes_time_down_outras_empresas.xlsx')

caminho_Clientes_time_down_xlsx = os.path.join(BASE_DIR, 'applications','equipments','datacom','Excel','Clientes_down_time.xlsx')