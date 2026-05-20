import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager

print("Iniciando o extrator com os novos passos para Guapimirim...")

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
espera = WebDriverWait(navegador, 20)

try:
    # --- PASSO 1: EXTRAIR RECEITA ---
    print("Acessando a página de Receitas...")
    navegador.get("https://guapimirimtp.portalfacil.com.br/receitas-por-meses")
    time.sleep(5) 
    
    # 1. Clicar em "Filtrar pesquisa"
    botao_abrir_filtros_rec = espera.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filtro"]/h3/a')))
    botao_abrir_filtros_rec.click()
    time.sleep(2) 
    
    # 2. Selecionar o ano na lista "Exercício"
    campo_ano_rec = espera.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pesquisa-ano-slAno"]')))
    menu_rec = Select(campo_ano_rec)
    menu_rec.select_by_visible_text("2023") 
    
    # 3. Clicar no botão final "Filtrar"
    botao_aplicar_rec = espera.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pesquisar-botao"]')))
    botao_aplicar_rec.click()
    
    # 4. Esperar carregar e capturar o valor
    time.sleep(5) 
    valor_receita = espera.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="datatable"]/tbody/tr[1]/td[4]'))).text
    
    # --- PASSO 2: EXTRAIR DESPESA ---
    print("Acessando a página de Despesas...")
    navegador.get("https://guapimirimtp.portalfacil.com.br/despesas-por-elementos")
    time.sleep(5)
    
    botao_abrir_filtros_desp = espera.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filtro"]/h3/a')))
    botao_abrir_filtros_desp.click()
    time.sleep(2)
    
    campo_ano_desp = espera.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pesquisa-ano-slAno"]')))
    menu_desp = Select(campo_ano_desp)
    menu_desp.select_by_visible_text("2023")
    
    botao_aplicar_desp = espera.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pesquisar-botao"]')))
    botao_aplicar_desp.click()
    
    time.sleep(5)
    valor_despesa = espera.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="datatable"]/tbody/tr[1]/td[5]'))).text
    
    # --- PASSO 3: EXTRAIR ROYALTIES ---
    print("Acessando a página de Royalties...")
    navegador.get("https://guapimirimtp.portalfacil.com.br/tpc_rec_mes_vis.aspx?exercicio=2023&idReceita=1.0.0.0.00.00.00&dsReceita=Receitas%20Correntes&idEntidade=1&dsEntidade=PREFEITURA%20MUNICIPAL%20DE%20GUAPIMIRIM%20-%20RJ")
    time.sleep(5)
    
    # 1. Encontrar o campo "Pesquisar" e digitar "royalties"
    campo_pesquisa = espera.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="datatable_filter"]/label/input')))
    campo_pesquisa.send_keys("royalties")
    
    # 2. Apertar ENTER para iniciar a busca 
    campo_pesquisa.send_keys(Keys.ENTER)
    
    # 3. Esperar a tabela atualizar e extrair o número
    time.sleep(5)
    valor_royalties = espera.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="datatable"]/tbody/tr[3]/td[4]'))).text
    
    print("\nExtração concluída com sucesso!")
    print(f"Receita Total: {valor_receita}")
    print(f"Despesa Total: {valor_despesa}")
    print(f"Royalties: {valor_royalties}")

except Exception as erro:
    print(f"\nErro na extração. Detalhe: {erro}")

finally:
    navegador.quit()
