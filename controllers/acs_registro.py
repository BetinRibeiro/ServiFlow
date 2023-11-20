# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    """
    Função: index
    Descrição: Lista os registro_financeiros relacionados a uma empresa com opções de paginação e filtragem.

    Fluxo de Funcionamento:
    1. Verifica o usuário e a empresa associada.
    2. Redireciona para a página inicial se o usuário estiver inativo.
    3. Configurações de paginação e verifica parâmetros da URL.
    4. Cálculo de páginas e limites para exibição dos registros.
    5. Consulta os registros de registro_financeiros da empresa, incluindo opção de filtro por pesquisa.
    6. Retorna os dados para a visualização na página.

    Parâmetros:
    - Não há parâmetros específicos além dos padrões do web2py.

    Retorna:
    - Um dicionário contendo os registros de registro_financeiros encontrados, informações de paginação e detalhes da empresa para a visualização na página.

    Requisitos:
    - O usuário deve estar logado para acessar esta funcionalidade.
    """
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Redireciona para a página inicial se o usuário estiver inativo
    if usuario.ativo == False:
        redirect(URL('default', 'index'))

    # Configurações de paginação e verificação dos parâmetros da URL
    paginacao = empresa.paginacao
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL(args=[1]))

    # Lógica de cálculo de páginas e limites
    if pagina <= 0:
        pagina = 1
    total = db((db.registro_financeiro.empresa == empresa.id)).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))

    # Consulta os registros dos registro_financeiros da empresa, incluindo filtro de pesquisa
    registros = db((db.registro_financeiro.empresa == empresa.id)).select(
        limitby=limites, orderby=~db.registro_financeiro.id | db.registro_financeiro.descricao)
    consul = request.args(1)
    if consul:
        registros = db((db.registro_financeiro.empresa == empresa.id) & (
            (db.registro_financeiro.nome.contains(consul)) | (db.registro_financeiro.descricao.contains(consul)))).select(
            limitby=limites, orderby=db.registro_financeiro.nome)

    # Retorna os dados para a visualização
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)


@auth.requires_login()
def cadastrar():
    """
    Função: cadastrar
    Descrição: Realiza o cadastro de um novo registro_financeiro.

    Fluxo de Funcionamento:
    1. Busca o usuário e a empresa associada.
    2. Configura a visualização e define o título da página.
    3. Define o valor padrão da empresa no formulário de cadastro do registro_financeiro.
    4. Processa o formulário de cadastro do registro_financeiro.
    5. Redireciona para a página principal após aceitar o formulário.
    6. Exibe uma mensagem de erro se o formulário não for aceito.

    Parâmetros:
    - Não há parâmetros específicos além dos padrões do web2py.

    Retorna:
    - Um dicionário contendo o formulário para o cadastro de registro_financeiro.

    Requisitos:
    - O usuário deve estar logado para acessar esta funcionalidade.
    """
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Cadastro de registro_financeiro'  # define o título da página
    tipo = request.args(0, cast=int)
    
    if tipo==1:
        db.registro_financeiro.cliente.writable=True
        db.registro_financeiro.cliente.readable=True
        db.registro_financeiro.cliente.requires = IS_IN_DB(db((db.cliente.empresa==empresa.id)&(db.cliente.ativo==True)), 'cliente.id', '%(nome)s - %(placa)s')
        db.registro_financeiro.servico.writable=True
        db.registro_financeiro.servico.readable=True
        db.registro_financeiro.servico.requires = IS_IN_DB(db((db.servico.empresa==empresa.id)&(db.servico.ativo==True)), 'servico.id', '%(nome)s - %(descricao)s')
        db.registro_financeiro.tipo.default='Entrada'
        db.registro_financeiro.classificacao.default='Receita de Vendas'
        db.registro_financeiro.classificacao.requires = IS_IN_SET(['Receita de Vendas','Outra'])
    else:
        db.registro_financeiro.tipo.default='Saida'
        db.registro_financeiro.classificacao.default='Despesa Administrativa'
        db.registro_financeiro.classificacao.writable=True
        db.registro_financeiro.classificacao.readable=True
        db.registro_financeiro.classificacao.requires = IS_IN_SET(['Despesa Administrativa','Despesa de Venda','Pagamento Produto ','Despesa Financeira','Despesa Pessoal'])

    # Define o valor padrão da empresa no formulário e processa o formulário
    db.registro_financeiro.empresa.default = usuario.empresa
    form = SQLFORM(db.registro_financeiro).process()

    # Redireciona para a página principal após aceitar o formulário
    if form.accepted:
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulário não aceito'  # exibe uma mensagem de erro se o formulário não for aceito

    # Retorna o formulário para a visualização
    return dict(form=form)

@auth.requires_login()
def alterar():
    """
    Função: alterar
    Descrição: Permite a alteração de um registro_financeiro existente.

    Fluxo de Funcionamento:
    1. Busca o usuário e o registro_financeiro relacionado.
    2. Verifica se o registro_financeiro pertence à empresa do usuário logado.
    3. Configurações da visualização e definição do título da página.
    4. Cria e processa o formulário de alteração do registro_financeiro.
    5. Redireciona para a página principal após a aceitação do formulário.
    6. Exibe uma mensagem de erro se o formulário não for aceito.

    Parâmetros:
    - Não há parâmetros específicos além dos padrões do web2py.

    Retorna:
    - Um dicionário contendo o formulário para a alteração do registro_financeiro.

    Requisitos:
    - O usuário deve estar logado para acessar esta funcionalidade.
    """

    # Busca o usuário e registro_financeiro relacionado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    registro_financeiro = db.registro_financeiro(request.args(0, cast=int))
    empresa = db.empresa(registro_financeiro.empresa)

    db.registro_financeiro.empresa.readable=False
    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])

    # Redireciona se o registro_financeiro não pertencer à empresa do usuário
    if registro_financeiro.empresa != usuario.empresa:
        redirect(URL('index'))

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Alterar registro_financeiro'  # define o título da página
    if registro_financeiro.tipo=="Entrada":
        db.registro_financeiro.cliente.writable=True
        db.registro_financeiro.cliente.readable=True
        db.registro_financeiro.cliente.requires = IS_IN_DB(db((db.cliente.empresa==empresa.id)&(db.cliente.ativo==True)), 'cliente.id', '%(nome)s - %(placa)s')
        db.registro_financeiro.servico.writable=True
        db.registro_financeiro.servico.readable=True
        db.registro_financeiro.servico.requires = IS_IN_DB(db((db.servico.empresa==empresa.id)&(db.servico.ativo==True)), 'servico.id', '%(nome)s - %(descricao)s')
        db.registro_financeiro.tipo.default='Entrada'
        db.registro_financeiro.classificacao.default='Receita de Vendas'
        db.registro_financeiro.classificacao.requires = IS_IN_SET(['Receita de Vendas','Outra'])
    else:
        db.registro_financeiro.cliente.readable=False
        db.registro_financeiro.servico.readable=False
        db.registro_financeiro.tipo.default='Saida'
        db.registro_financeiro.classificacao.default='Despesa Administrativa'
        db.registro_financeiro.classificacao.writable=True
        db.registro_financeiro.classificacao.readable=True
        db.registro_financeiro.classificacao.requires = IS_IN_SET(['Despesa Administrativa','Despesa de Venda','Pagamento Produto ','Despesa Financeira','Despesa Pessoal'])
    # Cria e processa o formulário de alteração
    form = SQLFORM(db.registro_financeiro, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index', args=pagina))
    elif form.errors:
        response.flash = 'Formulário não aceito'  # exibe uma mensagem de erro se o formulário não for aceito

    # Retorna o formulário para a visualização
    return dict(form=form)


def liquidar_registro():
    registro_financeiro = db.registro_financeiro(request.args(0, cast=int))
    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])
    if registro_financeiro.liquidado==True:
        registro_financeiro.liquidado=False
    else:
        registro_financeiro.liquidado=True
    registro_financeiro.update_record()
    return redirect(URL('index', args=pagina))
