import ctypes
import logging

# Constants for different message box types
MB_OK = 0x0
MB_OKCANCEL = 0x1
MB_YESNO = 0x4

# Constants for different icon styles
ICON_EXLAIM = 0x30
ICON_INFO = 0x40
ICON_ERROR = 0x10
ICON_QUESTION = 0x20

#Configuração do logger
logger = logging.getLogger('my_logger') #Cria o objeto de log
logger.setLevel(logging.INFO) #Configura o nível de log
handler = logging.FileHandler('C:\\TinyProdUni\\log_file.log') #Cria arquivo handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S') #Define o formato do log
handler.setFormatter(formatter) #Define o formato do log para o handler
logger.addHandler(handler) #Adiciona o handler ao logger

def pop_up_erro(erro):
    ctypes.windll.user32.MessageBoxW(0, f"{erro}", "TinyERP - ERRO:", MB_OK | ICON_ERROR)

def pop_up_check(check):
    ctypes.windll.user32.MessageBoxW(0, f"{check}", "TinyERP - INFO:", MB_OK | ICON_INFO)

def log_erro(erro):
    logger.error(erro)

def log_info(info):
    logger.info(info)