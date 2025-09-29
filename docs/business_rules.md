# 📋 Regras de Negócio - E-commerce Database
## Documentação Baseada na Estrutura do Banco

## 👥 MÓDULO DE CLIENTES

### Regras de Cadastro (Tabela CLIENTES)
- *Tipo de Cliente Exclusivo:* Cada cliente deve ser PESSOA_FÍSICA ou PESSOA_JURIDICA, nunca ambos
- *Pessoa Física:* Obrigatório NOME e CPF, proibido RAZAO_SOCIAL e CNPJ
- *Pessoa Jurídica:* Obrigatório RAZAO_SOCIAL e CNPJ, proibido NOME e CPF
- *Email Único:* Não podem existir dois clientes com mesmo email
- *Formato de Email Válido:* Validação via expressão regular
- *Data de Cadastro Automática:* Registro do momento de criação

### Comportamentos dos Clientes
- Clientes podem fazer *1 ou mais pedidos* (relação 1:N com PEDIDOS)
- Clientes podem fazer *nenhum pedido* (apenas cadastrados)
- Clientes podem *efetuar pagamento ou não* (através de PAGAMENTOS)
- Clientes podem *fazer avaliações ou não* (através de AVALIACOES)

## 📍 MÓDULO DE ENDEREÇOS

### Regras de Endereço (Tabela ENDERECOS)
- *Vínculo Obrigatório:* Todo endereço pertence a um cliente existente
- *Tipos de Endereço:* RESIDENCIAL ou COMERCIAL
- *Multiplicidade:* Um cliente pode ter *um ou mais endereços*
- *Reutilização:* Mesmo endereço pode receber *múltiplas entregas*
- *Campos Obrigatórios:* LOGRADOURO, NUMERO, BAIRRO, CIDADE, ESTADO, CEP
- *Complemento Opcional:* Campo COMPLEMENTO pode ser NULL

## 📞 MÓDULO DE TELEFONES

### Regras de Contato (Tabela TELEFONES)
- *Vínculo Obrigatório:* Todo telefone pertence a um cliente existente
- *Tipos de Telefone:* CELULAR, COMERCIAL, RESIDENCIAL
- *Multiplicidade:* Clientes podem ter *um ou mais telefones*
- *Exclusão em Cascata:* Ao excluir cliente, telefones são removidos automaticamente

## 🛒 MÓDULO DE PEDIDOS

### Regras de Vendas (Tabela PEDIDOS)
- *Vínculo Obrigatório:* Todo pedido pertence a um cliente existente
- *Status Controlado:* PENDENTE, PAGO ou CANCELADO
- *Status Padrão:* Novo pedido inicia como PENDENTE
- *Valor Total Obrigatório:* VALOR_TOTAL deve ser informado
- *Data Automática:* DATA_PEDIDO registrada no momento da criação
- *Exclusão em Cascata:* Ao excluir cliente, pedidos são removidos

### Cenários de Pedido
- Pedidos podem ter *entrega ou não* (retirada no local)
- Pedidos podem conter *um ou mais produtos* (através de ITENS_PEDIDOS)
- Pedidos podem ter *pagamento efetivado ou não*

## 📋 MÓDULO DE ITENS DE PEDIDO

### Regras de Composição (Tabela ITENS_PEDIDOS)
- *Vínculo Duplo:* Item pertence a pedido e produto existentes
- *Quantidade Mínima:* QUANTIDADE deve ser maior que zero
- *Preço Capturado:* PRECO_UNITARIO é registrado no momento da venda
- *Subtotal Automático:* Calculado como preço × quantidade (coluna gerada)

## 💰 MÓDULO DE PAGAMENTOS

### Regras Financeiras (Tabela PAGAMENTOS)
- *Vínculo Obrigatório:* Todo pagamento pertence a um pedido existente
- *Métodos Aceitos:* CARTÃO, BOLETO, PIX
- *Status Controlado:* APROVADO, RECUSADO, PENDENTE
- *Valor Obrigatório:* VALOR_PAGO deve ser informado
- *Data Automática:* DATA_PAGAMENTO registrada no momento do pagamento

### Cenários de Pagamento
- Pagamentos podem ser *efetuados ou não*
- Pagamentos podem ser *aprovados, recusados ou pendentes*
- Diferentes métodos de pagamento são suportados

## 🚚 MÓDULO DE ENTREGAS

### Regras Logísticas (Tabela ENTREGAS)
- *Vínculo Duplo:* Entrega pertence a pedido e endereço existentes
- *Status Controlado:* PREPARAÇÃO, ENVIADO, EM_TRANSITO, ENTREGUE, CANCELADO
- *Transportadora Obrigatória:* Nome da transportadora deve ser informado
- *Rastreamento Obrigatório:* CODIGO_RASTREAMENTO é obrigatório

### Gestão de Prazos
- *Datas Flexíveis:* DATA_ENVIO, DATA_PREVISTA, DATA_ENTREGA podem ser NULL
- *Entregas no Mesmo Endereço:* Endereço pode receber múltiplas entregas
- *Cancelamento:* Entregas podem ser canceladas
- *Atrasos/Antecipações:* Entrega pode chegar antes ou depois da data prevista

## ⭐ MÓDULO DE AVALIAÇÕES

### Regras de Feedback (Tabela AVALIACOES)
- *Vínculo Duplo:* Avaliação pertence a cliente e produto existentes
- *Nota Limitada:* NOTA deve estar entre 1 e 5
- *Comentário Opcional:* COMENTARIO pode ser NULL
- *Data Automática:* DATA_AVALIACAO registrada no momento da avaliação

### Flexibilidade de Avaliação
- Clientes podem *optar por não avaliar*
- Avaliação pode conter *apenas nota*
- Avaliação pode conter *nota e comentário*
- Apenas clientes que compraram podem avaliar

## 📦 MÓDULO DE PRODUTOS E CATEGORIAS

### Regras de Catálogo (Tabela PRODUTOS)
- *Nome Único:* Não podem existir dois produtos com mesmo nome
- *Preço Positivo:* PRECO_UNITARIO deve ser maior que zero
- *Estoque Padrão:* QUANTIDADE_ESTOQUE inicia com zero
- *Vínculo com Categoria:* Produto pertence a categoria existente
- *Vínculo com Fornecedor:* Produto tem fornecedor existente
- *Data de Cadastro Automática:* Registrada no momento da criação

### Regras de Organização (Tabela CATEGORIAS)
- *Nome Único:* Não podem existir duas categorias com mesmo nome
- *Descrição Opcional:* DESCRICAO pode ser NULL

## 🏢 MÓDULO DE FORNECEDORES

### Regras de Parcerias (Tabela FORNECEDORES)
- *CNPJ Único:* Não podem existir dois fornecedores com mesmo CNPJ
- *Email Único:* Não podem existir dois fornecedores com mesmo email
- *Campos Obrigatórios:* NOME_FORNECEDOR, CNPJ, EMAIL, TELEFONE

## 🔒 REGRAS GERAIS DE INTEGRIDADE

### Constraints Implementadas
1. *TIPO_CHECK:* Validação consistente entre tipo de cliente e documentos
2. *EMAIL_VALIDO_CHECK:* Formato de email válido via regex
3. *PRECO_POSITIVO_CHECK:* Preços sempre positivos
4. *QUANTIDADE > 0:* Quantidade mínima de itens
5. *NOTA BETWEEN 1 AND 5:* Escala de avaliação limitada

### Relacionamentos Validados
- Todas as relações entre tabelas são validadas via FOREIGN KEY
- Exclusão em cascata apenas onde faz sentido (preserva histórico financeiro)

### Valores Únicos Garantidos
- CLIENTES.EMAIL, CLIENTES.CPF, CLIENTES.CNPJ
- CATEGORIAS.NOME_CATEGORIA
- FORNECEDORES.CNPJ, FORNECEDORES.EMAIL
- PRODUTOS.NOME_PRODUTO

## ⏰ REGRAS TEMPORAIS

### Datas Automáticas
- CLIENTES.DATA_CADASTRO
- PRODUTOS.DATA_CADASTRO
- PEDIDOS.DATA_PEDIDO
- PAGAMENTOS.DATA_PAGAMENTO
- AVALIACOES.DATA_AVALIACAO

## 📊 CENÁRIOS DE NEGÓCIO SUPORTADOS

### Cliente com Comportamento Completo
- Faz múltiplos pedidos com diferentes endereços
- Usa diferentes métodos de pagamento
- Faz avaliações com e sem comentários
- Tem múltiplos telefones cadastrados

### Cliente com Pedido Problemático
- Faz pedido mas não efetua pagamento (PENDENTE → CANCELADO)
- Não solicita entrega (retirada no local)
- Não faz avaliação dos produtos

### Cliente Corporativo
- Pessoa Jurídica com múltiplos endereços comerciais
- Faz pedidos volumosos com vários produtos
- Usa diferentes endereços para faturação e entrega
