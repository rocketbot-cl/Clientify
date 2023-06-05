# Clientify
  
Modulo para interagir com Clientify.  

*Read this in other languages: [English](Manual_Clientify.md), [Português](Manual_Clientify.pr.md), [Español](Manual_Clientify.es.md)*
  
![banner](imgs/Banner_Clientify.png)
## Como instalar este módulo
  
Para instalar o módulo no Rocketbot Studio, pode ser feito de duas formas:
1. Manual: __Baixe__ o arquivo .zip e descompacte-o na pasta módulos. O nome da pasta deve ser o mesmo do módulo e dentro dela devem ter os seguintes arquivos e pastas: \__init__.py, package.json, docs, example e libs. Se você tiver o aplicativo aberto, atualize seu navegador para poder usar o novo módulo.
2. Automático: Ao entrar no Rocketbot Studio na margem direita você encontrará a seção **Addons**, selecione **Install Mods**, procure o módulo desejado e aperte instalar.  


## Descrição do comando

### Conectar a Clientify
  
Conectar a Clientify
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Nome de usuário|Nome de usuário da conta Clientify|usuario|
|Senha|Senha da conta Clientify|********|
|Atribuir resultado à variável|Variável para atribuir o resultado. Ele trará um JSON.|Variável|

### Obter oportunidade com filtros
  
Obtém oportunidade com filtros
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Filtro específico|Filtro de pesquisa específico; por exemplo nome da oportunidade, nome da empresa, nome do contato, sobrenome do contato, oportunidade|Rocket|
|Nome do proprietário|Filtro de nome do proprietário|Charles|
|Filtro maior que|Seletor para usar com data de fechamento maior que||
|Data de fechamento|Data de fechamento maior que. Formato yyyy/mm/dd|2021/08/23|
|Filtro menor que|Seletor para usar com data de fechamento menor que||
|Data de fechamento|Data de fechamento menor que. Formato yyyy/mm/dd|2021/08/23|
|Estado|Estado da oportunidade. Ex Won (ganhou), Lost (perdeu).||
|Fluxo|Filtro de fluxo da oportunidade.|Venda|
|Tipo de filtro de data|Filtro de data, criada ou modificada.||
|Filtro maior que|Seletor para usar com data de criação ou modificação maior que.||
|Data|Data de criação ou modificação maior que. Formato yyyy/mm/dd|2021/08/23|
|Filtro menor que|Seletor para usar com data de criação ou modificação menor que.||
|Data|Data de criação ou modificação menor que. Formato yyyy/mm/dd|2021/08/23|
|Atribuir resultado à variável|Variável à qual atribuir o resultado. Trazerá um JSON.|Variável|

### Obter oportunidade por ID
  
Obtém todas as propriedades de uma oportunidade por ID
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID da oportunidade|ID da oportunidade. Você pode obtê-lo listando os comandos de oportunidades ou na url em Clientify|2704232|
|Atribuir resultado à variável|Variável à qual atribuir o resultado. Trazerá um JSON.|Variável|

### Obter produtos
  
Este comando permite obter todos os produtos do Clientify
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Atribuir resultado à variável|Variável à qual atribuir o resultado.|Variável|

### Obter empresas por query
  
Este comando permite obter empresas por nome, data de criação ou data de modificação
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Tipo de filtro|Tipo de filtro a aplicar. Se for selecionada a Data de criação ou a Data de modificação, trará todas as empresas que tenham sido criadas ou modificadas depois da data selecionada.||
|Valor a buscar|Valor a buscar no filtro.|Rocketbot|
|Atribuir resultado a variável|Variável à qual atribuir o resultado.|Variável|

### Obter contatos por query
  
Este comando permite obter contatos por nome, telefone ou email.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Tipo de filtro|Tipo de filtro a aplicar.||
|Valor a buscar|Valor a buscar no filtro.|example@rocketbot.com|
|Atribuir resultado à variável|Variável à qual atribuir o resultado.|Variável|

### Criar oportunidade
  
Este comando permite criar uma oportunidade.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Nome da oportunidade|Nome da oportunidade a criar.|venda|
|Valor da oportunidade|Valor da oportunidade a criar.|1500|
|ID do contato|ID do contato ao qual atribuir a oportunidade.|39562459|
|ID da companhia|ID da companhia à qual atribuir a oportunidade.|39562459|
|Data de fechamento|Data de fechamento da oportunidade.|2023-03-20|
|Produtos|Lista de produtos da oportunidade.|[{"product_id":"4048412","quantity":1}, {"product_id":"4048413","quantity":2}]|
|Custom fields|Lista de campos personalizados da oportunidade.|#TODO|
|Atribuir resultado à variável|Variável à qual atribuir o resultado.|Variável|
