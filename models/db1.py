# -*- coding: utf-8 -*-

db.define_table('servico',
                Field('empresa', 'reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', writable=True, readable=True, label='Nome' ,default='',requires = IS_UPPER()),
                Field('descricao', 'string', writable=True, readable=True, label='Descrição' ,default='',requires = IS_UPPER()),
                Field('valor', 'double', writable=False, readable=False,  notnull=True, default=0),
                Field('observacao', 'text', writable=True, readable=True, label='Observação' ,default='',requires = IS_UPPER()),
                Field('ativo', 'boolean', writable=True, readable=True, default=True, label='Ativo'),
                auth.signature,
                format='%(nome)s')

db.servico.id.writable=False
db.servico.id.readable=False

db.define_table('cliente',
                Field('empresa', 'reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', writable=True, readable=True, label='Nome' ,default='',requires = IS_UPPER()),
                Field('fone', 'string', writable=True, readable=True, label='Fone' ,default='',requires = IS_UPPER()),
                Field('placa', 'string', writable=True, readable=True, label='Placa' ,default='',requires = IS_UPPER()),
                Field('marca', 'string', writable=True, readable=True, label='Marca' ,default='',requires = IS_UPPER()),
                Field('modelo', 'string', writable=True, readable=True, label='Modelo' ,default='',requires = IS_UPPER()),
                Field('observacao', 'text', writable=True, readable=True, label='Observação' ,requires = IS_UPPER()),
                Field('valor_total', 'double', writable=False, readable=False,  notnull=True, default=0),
                Field('ativo', 'boolean', writable=True, readable=True, default=True, label='Ativo'),
                auth.signature,
                format='%(nome)s')


db.cliente.id.writable=False
db.cliente.id.readable=False
db.cliente.marca.requires = IS_IN_SET(lista_marcas())

db.define_table('registro_financeiro',
                Field('empresa','reference empresa', writable=False, readable=True, label='Empresa'),
                Field('servico','reference servico', writable=False, readable=True,  label='Serviço'),
                Field('cliente','reference cliente', writable=False, readable=True, label='Cliente'),
                Field('tipo', 'string', writable=False, readable=True, label='Tipo' ,default=''),
                Field('classificacao', 'string', writable=False, readable=True, label='Classificação' ,default=''),
                Field('data_operacao', 'date', writable=True, readable=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('data_recebimento', 'date', writable=True, readable=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string',label='Descrição', writable=True, notnull=True,requires = IS_UPPER()),
                Field('valor_total', 'double',label='Valor', notnull=True, default=0),
                Field('liquidado', 'boolean', writable=True, readable=True, default=False),
                Field('excluido', 'boolean', writable=False, readable=False, default=False, label='Excluir'),
                auth.signature,
                format='%(descricao)s')

db.registro_financeiro.id.writable=False
db.registro_financeiro.id.readable=False
db.registro_financeiro.tipo.requires = IS_IN_SET(['Entrada','Saida'])
db.registro_financeiro.classificacao.requires = IS_IN_SET(['Receita de Vendas','Despesa Administrativa','Despesa de Venda','Pagamento Produto ','Despesa Financeira','Despesa Pessoal'])
