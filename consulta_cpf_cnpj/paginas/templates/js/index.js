var verificaTipo = "";

$(document).ready(function(){
    $("#cpf").mask("999.999.999-99");
    $("#cnpj").mask("99.999.999/9999-99");
});

$("#cnpj").change(function(event){
    event.preventDefault();
    if($("#cnpj").val() != ""){
        $("#consulta_cnpj").prop("disabled", false);
    }else{
        $("#consulta_cnpj").prop("disabled", true);
    }
});

$("#cpf, #data_nasc").change(function(event){
    event.preventDefault();
    if($("#cpf").val() != "" && $("#data_nasc").val() != ""){
        $("#consulta_cpf").prop("disabled", false);
    }else{
        $("#consulta_cpf").prop("disabled", true);
    }
});

$("#consulta_cpf").click(function(event){
    event.preventDefault();
    $(".loader").toggle();
    $.get("/get_captcha_cpf", {}, function(response){
        response = JSON.parse(response);
        if(response.mensagem == "OK"){
            $("#modalTitle").html("Autenticar");
            var timestamp = new Date().getTime(); 
            $('#body-modal-receita').html(`
                <div class="row row-center">
                    <div class="col-md-12">
                        <img id="img-captcha" src="/static/img/captcha_cpf.png?t=${timestamp}"></img>
                    </div>
                </div>
                <br>
                <div class="row row-center">
                    <div class="col-md-12">
                        <input type="text" id="text-captcha" placeholder="Digite os caracteres da imagem acima" onchange="liberaConsulta()"/>
                    </div>
                </div>
            `);
            $("#btn-save").css("visibility", "visible");
            $('#modal-receita').modal('show');
            verificaTipo = "cpf";
        }else{
            console.log(response.erro);
            alert("Erro interno! Tente novamente mais tarde.");
        }
        $(".loader").toggle();
    });
});

$("#consulta_cnpj").click(function(event){
    event.preventDefault();
    $(".loader").toggle();
    $.get("/get_captcha_cnpj", {}, function(response){
        response = JSON.parse(response);
        if(response.mensagem == "OK"){
            $("#modalTitle").html("Autenticar");
            var timestamp = new Date().getTime(); 
            $('#body-modal-receita').html(`
                <div class="row row-center">
                    <div class="col-md-12">
                        <img id="img-captcha" src="/static/img/captcha_cnpj.png?t=${timestamp}"></img>
                    </div>
                </div>
                <br>
                <div class="row row-center">
                    <div class="col-md-12">
                        <input type="text" id="text-captcha" placeholder="Digite os caracteres da imagem acima" onchange="liberaConsulta()"/>
                    </div>
                </div>
            `);
            $("#btn-save").css("visibility", "visible");
            $('#modal-receita').modal('show');
            verificaTipo = "cnpj";
        }else{
            alert("Erro interno! Tente novamente mais tarde.");
        }
        $(".loader").toggle();
    });
});

$("#btn-save").click(function(event){
    event.preventDefault();
    if(verificaTipo == "cpf"){
        $('#modal-receita').modal('hide');
        $(".loader").toggle();
        $.get("/consulta_cpf", {
            cpf: $("#cpf").val(),
            data_nasc: $("#data_nasc").val(),
            captcha: $("#text-captcha").val()
        }, function(response){
            response = JSON.parse(response);
            if(response.mensagem == "OK"){
                $("#modalTitle").html("Dados da pessoa física");
                $('#body-modal-receita').html(`
                    <textarea class="form-control" id="jsondata" rows="7" cols="50" readonly>
                    CPF: ${response.pessoa_fisica.cpf}
                    Nome completo: ${response.pessoa_fisica.nome}
                    Data de inscrição: ${response.pessoa_fisica.data_inscricao}
                    Data de nascimento: ${response.pessoa_fisica.data_nascimento}
                    Situação cadastral: ${response.pessoa_fisica.situacao_cadastral}
                    Digito verificador: ${response.pessoa_fisica.digito_verificador}
                    </textarea>
                `);
                $("#btn-save").css("visibility", "hidden");
                $('#modal-receita').modal('show');
            }else{
                $("#modalTitle").html("Atenção");
                $('#body-modal-receita').html(`
                    <div class="row row-center">
                        <h2 class="modal-title">
                            Erro na consulta! Digite os dados corretamente.
                        </h2> 
                    </div>
                `);
                $('#modal-receita').modal('show');
                $("#btn-save").css("visibility", "hidden");
            }
            $(".loader").toggle();
        });
    }else if(verificaTipo == "cnpj"){
        $('#modal-receita').modal('hide');
        $(".loader").toggle();
        $.get("/consulta_cnpj", {
            cnpj: $("#cnpj").val(),
            captcha: $("#text-captcha").val()
        }, function(response){
            response = JSON.parse(response);
            if(response.mensagem == "OK"){
                $("#modalTitle").html("Dados da pessoa jurídica");
                $('#body-modal-receita').html(`
                    <textarea class="form-control" id="jsondata" rows="7" cols="50" readonly>
                    CNPJ: ${response.pessoa_juridica.cnpj}
                    Nome empresarial: ${response.pessoa_juridica.nome_empresarial}
                    Nome fantasia: ${response.pessoa_juridica.nome_fantasia}
                    Tipo da empresa: ${response.pessoa_juridica.tipo_empresa}
                    Data de abertura: ${response.pessoa_juridica.data_abertura}
                    E-mail: ${response.pessoa_juridica.email}
                    Telefone: ${response.pessoa_juridica.telefone}
                    Situação cadastral: ${response.pessoa_juridica.situacao_cadastral}
                    Data da situação cadastral: ${response.pessoa_juridica.data_situacao_cadastral}
                    Logradouro: ${response.pessoa_juridica.endereco.logradouro}
                    Número: ${response.pessoa_juridica.endereco.numero}
                    Complemento: ${response.pessoa_juridica.endereco.complemento}
                    CEP: ${response.pessoa_juridica.endereco.cep}
                    Bairro: ${response.pessoa_juridica.endereco.bairro}
                    Município: ${response.pessoa_juridica.endereco.municipio}
                    Estado: ${response.pessoa_juridica.endereco.estado}
                    </textarea>
                `);
                $("#btn-save").css("visibility", "hidden");
                $('#modal-receita').modal('show');
            }else{
                $("#modalTitle").html("Atenção");
                $('#body-modal-receita').html(`
                    <div class="row row-center">
                        <h2 class="modal-title">
                            Erro na consulta! Digite os dados corretamente.
                        </h2> 
                    </div>
                `);
                $('#modal-receita').modal('show');
                $("#btn-save").css("visibility", "hidden");
            }
            $(".loader").toggle();
        });
    }
});

function liberaConsulta(){
    if($("#text-captcha").val() != ""){
        $("#btn-save").prop("disabled", false);
    }else{
        $("#btn-save").prop("disabled", true);
    }
}

$("#sobre").click(function(event){
    event.preventDefault();
    $("#modalTitle").html("Sobre");
    $("#btn-save").css("visibility", "hidden");
    $('#body-modal-receita').html(`
        <div class="container">
            <div class="row">
                <p class="paragraph">
                    Este site tem como objetivo realizar a integração entre a biblioteca Selenium e o
                    Framework Django da linguagem Python. O projeto utiliza técnicas de Web-Scraping
                    para fazer as consultas diretamente no site da Receita Federal, tornando-se independente
                    de API's pagas e que utilizam as bases de dados disponibilizadas pela Receita.
                    <br><br>
                    <a href="https://www.gov.br/receitafederal/pt-br">Site da Receita Federal</a>
                    <br>
                    <a href="https://github.com/JnCM/web-scrapping-consulta-receita">Código fonte</a>
                    <br>
                    <a href="https://www.tecmundo.com.br/internet/215525-web-scraping-conheca-tecnica-coleta-dados.htm">Web-scraping</a>
                    <br>
                    <a href="https://www.selenium.dev/">Biblioteca Selenium</a>
                    <br>
                    <a href="https://www.selenium.dev/">Framework Django</a>
                </p> 
            </div>
        </div>
    `);
    $('#modal-receita').modal('show');
});