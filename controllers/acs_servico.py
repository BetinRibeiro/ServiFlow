# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    """
    Função: index
    Descrição: Lista os serviços relacionados a uma empresa com opções de paginação e filtragem.

    Fluxo de Funcionamento:
    1. Verifica o usuário e a empresa associada.
    2. Redireciona para a página inicial se o usuário estiver inativo.
    3. Configurações de paginação e verifica parâmetros da URL.
    4. Cálculo de páginas e limites para exibição dos registros.
    5. Consulta os registros de serviços da empresa, incluindo opção de filtro por pesquisa.
    6. Retorna os dados para a visualização na página.

    Parâmetros:
    - Não há parâmetros específicos além dos padrões do web2py.

    Retorna:
    - Um dicionário contendo os registros de serviços encontrados, informações de paginação e detalhes da empresa para a visualização na página.

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
    total = db((db.servico.empresa == empresa.id)).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))

    # Consulta os registros dos serviços da empresa, incluindo filtro de pesquisa
    registros = db((db.servico.empresa == empresa.id)).select(
        limitby=limites, orderby=~db.servico.id | db.servico.nome)
    consul = request.args(1)
    if consul:
        registros = db((db.servico.empresa == empresa.id) & (
            (db.servico.nome.contains(consul)) | (db.servico.descricao.contains(consul)))).select(
            limitby=limites, orderby=db.servico.nome)

    # Retorna os dados para a visualização
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)


@auth.requires_login()
def cadastrar():
    """
    Função: cadastrar
    Descrição: Realiza o cadastro de um novo serviço.

    Fluxo de Funcionamento:
    1. Busca o usuário e a empresa associada.
    2. Configura a visualização e define o título da página.
    3. Define o valor padrão da empresa no formulário de cadastro do serviço.
    4. Processa o formulário de cadastro do serviço.
    5. Redireciona para a página principal após aceitar o formulário.
    6. Exibe uma mensagem de erro se o formulário não for aceito.

    Parâmetros:
    - Não há parâmetros específicos além dos padrões do web2py.

    Retorna:
    - Um dicionário contendo o formulário para o cadastro de serviço.

    Requisitos:
    - O usuário deve estar logado para acessar esta funcionalidade.
    """
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Cadastro de serviço'  # define o título da página

    # Define o valor padrão da empresa no formulário e processa o formulário
    db.servico.empresa.default = usuario.empresa
    form = SQLFORM(db.servico).process()

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
    Descrição: Permite a alteração de um serviço existente.

    Fluxo de Funcionamento:
    1. Busca o usuário e o serviço relacionado.
    2. Verifica se o serviço pertence à empresa do usuário logado.
    3. Configurações da visualização e definição do título da página.
    4. Cria e processa o formulário de alteração do serviço.
    5. Redireciona para a página principal após a aceitação do formulário.
    6. Exibe uma mensagem de erro se o formulário não for aceito.

    Parâmetros:
    - Não há parâmetros específicos além dos padrões do web2py.

    Retorna:
    - Um dicionário contendo o formulário para a alteração do serviço.

    Requisitos:
    - O usuário deve estar logado para acessar esta funcionalidade.
    """

    # Busca o usuário e serviço relacionado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    servico = db.servico(request.args(0, cast=int))

    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])

    # Redireciona se o serviço não pertencer à empresa do usuário
    if servico.empresa != usuario.empresa:
        redirect(URL('index'))

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = 'Alterar serviço'  # define o título da página

    # Cria e processa o formulário de alteração
    form = SQLFORM(db.servico, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index', args=pagina))
    elif form.errors:
        response.flash = 'Formulário não aceito'  # exibe uma mensagem de erro se o formulário não for aceito

    # Retorna o formulário para a visualização
    return dict(form=form)
