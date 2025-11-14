"""
Testes de Caixa Preta para o Sistema Unificado Completo.
Testa todos os módulos integrados através da interface web usando Selenium.
Este é o arquivo principal de testes E2E com Selenium.
"""
import pytest
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class TestSistemaCompleto:
    """Testes de caixa preta para o sistema unificado completo."""
    
    def test_home_page_loads(self, driver, base_url, wait):
        """Testa se a página inicial carrega corretamente."""
        driver.get(base_url)
        
        # Verificar se a página carregou
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "Sistema Unificado" in driver.title or "Grupo A" in driver.page_source
        
        # Verificar se há links para os módulos
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_pits_module_accessible(self, driver, base_url, wait):
        """Testa se o módulo PITS está acessível."""
        driver.get(f"{base_url}/pits/menu")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_trabalho2s_module_accessible(self, driver, base_url, wait):
        """Testa se o módulo Trabalho-2S está acessível."""
        driver.get(f"{base_url}/t2s/menu")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_emprestimo_module_accessible(self, driver, base_url, wait):
        """Testa se o módulo de Empréstimo está acessível."""
        driver.get(f"{base_url}/emprestimos")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_dacio_module_accessible(self, driver, base_url, wait):
        """Testa se o módulo Dácio está acessível."""
        driver.get(f"{base_url}/dacio/menu")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_api_loans_returns_json(self, driver, base_url):
        """Testa se a API de empréstimos retorna JSON válido."""
        driver.get(f"{base_url}/api/loans")
        
        # Verificar se retornou JSON
        body_text = driver.find_element(By.TAG_NAME, "body").text
        
        try:
            data = json.loads(body_text)
            assert isinstance(data, list)
        except json.JSONDecodeError:
            pytest.fail("API não retornou JSON válido")
    
    def test_navigation_between_modules(self, driver, base_url, wait):
        """Testa navegação entre diferentes módulos do sistema."""
        # Ir para página inicial
        driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Navegar para PITS
        driver.get(f"{base_url}/pits/usuarios")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "pits" in driver.current_url
        
        # Navegar para Trabalho-2S
        driver.get(f"{base_url}/t2s/menu")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "t2s" in driver.current_url
        
        # Navegar para Empréstimos
        driver.get(f"{base_url}/emprestimos")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "emprestimos" in driver.current_url
        
        # Navegar para Dácio
        driver.get(f"{base_url}/dacio/menu")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "dacio" in driver.current_url
    
    def test_trabalho2s_listar_usuarios(self, driver, base_url, wait):
        """Testa se a página de listagem de usuários do Trabalho-2S funciona."""
        driver.get(f"{base_url}/t2s/listar_usuarios")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_trabalho2s_listar_livros(self, driver, base_url, wait):
        """Testa se a página de listagem de livros do Trabalho-2S funciona."""
        driver.get(f"{base_url}/t2s/listar_livros")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_trabalho2s_listar_emprestimos(self, driver, base_url, wait):
        """Testa se a página de listagem de empréstimos do Trabalho-2S funciona."""
        driver.get(f"{base_url}/t2s/listar_emprestimos")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body = driver.find_element(By.TAG_NAME, "body")
        assert body is not None
    
    def test_trabalho2s_relatorios(self, driver, base_url, wait):
        """Testa se a página de relatórios do Trabalho-2S carrega."""
        driver.get(f"{base_url}/t2s/relatorios")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Verificar se há links para relatórios específicos
        try:
            livros_link = driver.find_element(By.XPATH, "//a[contains(@href, '/t2s/relatorios_livros')]")
            assert livros_link is not None
        except:
            # Se não encontrar por XPath, verificar se o texto está na página
            body_text = driver.find_element(By.TAG_NAME, "body").text
            assert "Relatórios" in body_text or "Analytics" in body_text
    
    def test_dacio_listar_livros(self, driver, base_url, wait):
        """Testa se a página de listagem de livros do Dácio funciona."""
        driver.get(f"{base_url}/dacio/listar_livros")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_dacio_cadastrar_livro_page(self, driver, base_url, wait):
        """Testa se a página de cadastro de livro do Dácio carrega."""
        driver.get(f"{base_url}/dacio/cadastrar_livro")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Verificar se há um formulário
        try:
            form = driver.find_element(By.TAG_NAME, "form")
            assert form is not None
        except:
            # Se não encontrar form, verificar se há inputs
            inputs = driver.find_elements(By.TAG_NAME, "input")
            assert len(inputs) > 0
    
    def test_devolucoes_page_loads(self, driver, base_url, wait):
        """Testa se a página de devoluções carrega corretamente."""
        driver.get(f"{base_url}/devolucoes")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 0
    
    def test_all_modules_integrated(self, driver, base_url, wait):
        """Testa se todos os módulos estão integrados e acessíveis."""
        modules = [
            ("/pits/menu", "PITS"),
            ("/t2s/menu", "Trabalho-2S"),
            ("/emprestimos", "Empréstimos"),
            ("/dacio/menu", "Dácio")
        ]
        
        for route, module_name in modules:
            try:
                driver.get(f"{base_url}{route}")
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                body_text = driver.find_element(By.TAG_NAME, "body").text
                assert len(body_text) > 0, f"Módulo {module_name} não retornou conteúdo"
            except Exception as e:
                pytest.fail(f"Erro ao acessar módulo {module_name}: {e}")

