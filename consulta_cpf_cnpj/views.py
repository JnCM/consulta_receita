from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import json # Para exibir o resultado da consulta
import urllib.request as urllib # Para salvar o captcha da página
import cv2 as cv # Para cortar o print da página
from . import utils

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def get_captcha_cpf(request):
    try:
        utils.setNewDriver()
        settings.SELENIUM_DRIVER.get(settings.URL_CPF)
        # Encontrando a imagem na página
        img = settings.SELENIUM_DRIVER.find_element("id", "imgCaptcha")
        # Pegando a URL da imagem
        src = img.get_attribute("src")
        # Salvando o captcha
        urllib.urlretrieve(src, "{}captcha_cpf.png".format(settings.PATH_TO_IMG))
        return HttpResponse(json.dumps({'mensagem': 'OK'}))
    except Exception as e:
        return HttpResponse(json.dumps({'mensagem': 'ERROR', 'erro': str(e)}))

def consulta_cpf(request):
    try:
        cpf = request.GET.get("cpf")
        data_nascimento = request.GET.get("data_nasc")
        data_nascimento = data_nascimento[8:10] + "/" + data_nascimento[5:7] + "/" + data_nascimento[0:4]
        captcha = request.GET.get("captcha")

        # Encontrando o campo de CPF
        input_cpf = settings.SELENIUM_DRIVER.find_element("id", "txtCPF")
        # Encontrando o campo de data de nascimento
        input_data_nasc = settings.SELENIUM_DRIVER.find_element("id", "txtDataNascimento")
        # Encontrando o campo de digitar o captcha
        input_captcha = settings.SELENIUM_DRIVER.find_element("id", "txtTexto_captcha_serpro_gov_br")

        # Escrevendo na página o CPF, data de nascimento e captcha recebidos
        settings.SELENIUM_DRIVER.execute_script("arguments[0].value='{}';".format(cpf), input_cpf)
        settings.SELENIUM_DRIVER.execute_script("arguments[0].value='{}';".format(data_nascimento), input_data_nasc)
        settings.SELENIUM_DRIVER.execute_script("arguments[0].value='{}';".format(captcha), input_captcha)

        # Realizando o submit do formulário da página da receita
        settings.SELENIUM_DRIVER.find_element("id", "theForm").submit()

        # Verifica se o resultado da consulta foi uma mensagem de erro
        temp = settings.SELENIUM_DRIVER.find_elements("class name", "clConteudoDados")
        
        if len(temp) == 0:
            settings.SELENIUM_DRIVER.quit()
            return HttpResponse(json.dumps({'mensagem': 'ERRO', 'erro': 'deu ruim'}))
        
        # Se não foi uma mensagem de erro, realiza o processo de obtenção dos resultados
        dados = []
        for t in temp:
            element = t.find_element("tag name", "b").text
            dados.append(element)

        # Monta o JSON que será retornado
        final_json = {
            "cpf": dados[0],
            "nome": dados[1],
            "data_nascimento": dados[2],
            "situacao_cadastral": dados[3],
            "data_inscricao": dados[4],
            "digito_verificador": dados[5]
        }

        settings.SELENIUM_DRIVER.quit()
        return HttpResponse(json.dumps({'mensagem': 'OK', 'pessoa_fisica': final_json}))
    except Exception as e:
        return HttpResponse(json.dumps({'mensagem': 'ERROR', 'erro': str(e)}))

def get_captcha_cnpj(request):
    try:
        utils.setNewDriver()
        settings.SELENIUM_DRIVER.get(settings.URL_CNPJ)
        # Salvando o print da página
        settings.SELENIUM_DRIVER.save_screenshot("{}screenshot.png".format(settings.PATH_TO_IMG))
        # Encontrando a imagem na página
        img = settings.SELENIUM_DRIVER.find_element("id", "imgCaptcha")
        # Armazenando as coordenadas (x,y) do captcha na tela
        loc = img.location
        # Realizando o processo de cortar a imagem do print
        image = cv.imread('{}screenshot.png'.format(settings.PATH_TO_IMG))
        desloc_x = 185
        desloc_y = 55
        cropped_image = image[loc['y']:loc['y']+desloc_y, loc['x']:loc['x']+desloc_x]
        cv.imwrite('{}captcha_cnpj.png'.format(settings.PATH_TO_IMG), cropped_image)

        return HttpResponse(json.dumps({'mensagem': 'OK'}))
    except:
        return HttpResponse(json.dumps({'mensagem': 'ERROR'}))

def consulta_cnpj(request):
    try:
        cnpj = request.GET.get("cnpj")
        captcha = request.GET.get("captcha")

        # Encontrando o campo de CNPJ
        input_cnpj = settings.SELENIUM_DRIVER.find_element("id", "cnpj")
        # Encontrando o campo de digitar o captcha
        input_captcha = settings.SELENIUM_DRIVER.find_element("id", "txtTexto_captcha_serpro_gov_br")

        # Escrevendo na página o CNPJ e captcha recebidos
        settings.SELENIUM_DRIVER.execute_script("arguments[0].value='{}';".format(cnpj), input_cnpj)
        settings.SELENIUM_DRIVER.execute_script("arguments[0].value='{}';".format(captcha), input_captcha)

        # Realizando o submit do formulário da página da receita
        settings.SELENIUM_DRIVER.find_element("id", "frmConsulta").submit()

        # Verifica se o resultado da consulta foi uma mensagem de erro
        temp = settings.SELENIUM_DRIVER.find_elements("tag name", "b")
        verifica = []
        for t in temp:
            verifica.append(t.text)
        if len(verifica) == 1:
            settings.SELENIUM_DRIVER.quit()
            return HttpResponse(json.dumps({'mensagem': 'ERRO'}))
        
        # Se não foi uma mensagem de erro, realiza o processo de obtenção dos resultados
        linha = settings.SELENIUM_DRIVER.find_elements("tag name", "font")
        for i in range(len(linha)):
            if linha[i].text == "NÚMERO DE INSCRIÇÃO":
                insc = linha[i+1].find_elements("tag name", "b")
                final_cnpj = insc[0].text
                tipo_empresa = insc[1].text
            elif linha[i].text == "DATA DE ABERTURA":
                data_abertura = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "NOME EMPRESARIAL":
                nome_empresarial = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "TÍTULO DO ESTABELECIMENTO (NOME DE FANTASIA)":
                nome_fantasia = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "LOGRADOURO":
                logradouro = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "NÚMERO":
                numero = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "COMPLEMENTO":
                complemento = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "CEP":
                cep = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "BAIRRO/DISTRITO":
                bairro = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "MUNICÍPIO":
                municipio = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "UF":
                estado = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "ENDEREÇO ELETRÔNICO":
                email = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "TELEFONE":
                telefone = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "SITUAÇÃO CADASTRAL":
                situacao_cadastral = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "DATA DA SITUAÇÃO CADASTRAL":
                data_situacao_cadastral = linha[i+1].find_element("tag name", "b").text

        # Monta o JSON que será retornado
        final_json = {
            "cnpj": final_cnpj,
            "tipo_empresa": tipo_empresa,
            "data_abertura": data_abertura,
            "nome_empresarial": nome_empresarial,
            "nome_fantasia": nome_fantasia,
            "endereco": {
                "logradouro": logradouro,
                "numero": numero,
                "complemento": complemento,
                "cep": cep,
                "bairro": bairro,
                "municipio": municipio,
                "estado": estado
            },
            "email": email,
            "telefone": telefone,
            "situacao_cadastral": situacao_cadastral,
            "data_situacao_cadastral": data_situacao_cadastral
        }

        settings.SELENIUM_DRIVER.quit()
        return HttpResponse(json.dumps({'mensagem': 'OK', 'pessoa_juridica': final_json}))
    except:
        return HttpResponse(json.dumps({'mensagem': 'ERROR'}))
