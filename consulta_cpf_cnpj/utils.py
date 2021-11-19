# Importação dos módulos necessários para a consulta
from selenium import webdriver # Necessário para inicializar o browser
from selenium.webdriver.chrome.service import Service # Mudar "edge" para o navegador em uso
from selenium.webdriver.chrome.options import Options # Mudar "edge" para o navegador em uso
from django.conf import settings

def setNewDriver():
    serv = Service(settings.PATH_TO_DRIVER)
    # Definindo as opções de utilização do selenium
    options = Options()
    # Desabilitando as mensagens do selenium no terminal (apenas erros serão exibidos)
    options.add_argument("--log-level=3")
    # Desabilitando a abertura automática de uma janela do navegador com a página da receita
    options.add_argument("--headless")
    options.binary_location = settings.BINARY_CHROME_PATH

    # Inicializando o selenium (MUDAR PARA O NAVEGADOR QUE FOR UTILIZAR)
    settings.SELENIUM_DRIVER = webdriver.Chrome(service=serv, service_log_path="NUL", options=options)
