"""
Configuração compartilhada para testes de caixa preta com Selenium.
"""
import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# Adicionar o diretório raiz ao path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Importar app Flask
from app import app as flask_app


@pytest.fixture(scope="session")
def flask_server():
    """Inicia o servidor Flask em uma thread separada para os testes."""
    import socket
    
    def check_port(host, port):
        """Verifica se a porta está disponível."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    
    def run_server():
        # Configurar app para não usar reloader
        flask_app.config['TESTING'] = True
        flask_app.run(host='127.0.0.1', port=5050, debug=False, use_reloader=False, threaded=True)
    
    # Verificar se porta já está em uso
    if check_port('127.0.0.1', 5050):
        print("⚠️  Porta 5050 já está em uso. Certifique-se de que o app não está rodando.")
        yield
        return
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Aguardar servidor iniciar (verificar se porta está respondendo)
    max_attempts = 10
    for i in range(max_attempts):
        if check_port('127.0.0.1', 5050):
            break
        time.sleep(0.5)
    else:
        pytest.fail("Servidor Flask não iniciou a tempo")
    
    # Aguardar um pouco mais para garantir que está pronto
    time.sleep(1)
    
    yield
    
    # Cleanup (servidor será encerrado quando a thread daemon terminar)


@pytest.fixture(scope="function")
def driver():
    """Cria e configura o driver Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # Tentar usar webdriver-manager
        driver_path = ChromeDriverManager().install()
        
        # Encontrar o executável correto (pode estar em subdiretório)
        import os
        import stat
        
        def find_chromedriver(path):
            """Encontra o executável chromedriver."""
            if os.path.isfile(path):
                # Verificar se é executável
                if os.access(path, os.X_OK) and 'chromedriver' in os.path.basename(path).lower():
                    return path
            elif os.path.isdir(path):
                # Procurar recursivamente
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if 'chromedriver' in file.lower() and not file.endswith('.txt') and not file.endswith('.md'):
                            full_path = os.path.join(root, file)
                            if os.access(full_path, os.X_OK):
                                return full_path
            return None
        
        # Tentar encontrar o executável
        chromedriver_exe = find_chromedriver(driver_path)
        if not chromedriver_exe:
            # Se não encontrar, tentar usar o caminho retornado diretamente
            chromedriver_exe = driver_path
        
        service = Service(chromedriver_exe)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        # Se falhar, tentar sem especificar o caminho (usar PATH do sistema)
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e2:
            pytest.skip(f"Não foi possível inicializar o ChromeDriver. Erro: {e2}. "
                       f"Certifique-se de que o Chrome está instalado.")
    
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()


@pytest.fixture
def base_url(flask_server):
    """URL base do servidor de teste."""
    return "http://127.0.0.1:5050"


@pytest.fixture
def wait(driver):
    """Helper para esperas explícitas."""
    return WebDriverWait(driver, 10)

