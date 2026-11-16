Universidade Federal do Vale do São Francisco  
Colegiado de Engenharia da Computação  
Sistemas Distribuídos

# Especificações de Projeto 

\[ comunicação direta / desenvolvimento web \]

## Descrição

Desenvolver sistema web em linguagem *Python* \+ *framework Django* com acesso e manipulação de objetos em bancos de dados relacionais.

**Pontos de destaque**

* a colaboração entre equipes é permitida e estimulada  
* o projeto será entregue em três momentos valendo 1 \+ 1 \+ 1 \+ 7  
  * Ideia e especificação inicial (10%)  
  * Modelos e Admin (10%)  
  * Visões e Formulários (10%)  
  * Entrega Final \- hospedado em cloud \+ domínio (70%)  
* a nota do projeto será composta pela entrega dos itens obrigatórios \+ apresentação final

## Entregas

### \[ 1.0 ponto \] Entrega I \- Descrição Inicial

* Artefato: especificação **simplificada** do projeto, conforme formulário no Google Classroom, contendo nome dos integrantes da equipe, título do projeto, resumo, lista esperada de modelos, lista esperada de funcionalidades.   
* Observação: não se trata de um contrato firmado, apenas uma especificação inicial de alto nível. Durante o processo de desenvolvimento, o grupo poderá alterar o escopo, sugerir novos modelos, modificar a lista de funcionalidades sugeridas, etc.

### \[ 1.0 ponto \] Entrega II \- Descrição Inicial

* Modelos e Administração

### \[ 1.0 ponto \] Entrega III \- Descrição Inicial

* Visões e Formulários

### \[ 7.0 pontos \] Entrega IV \- Apresentação Final

* Artefato: Apresentação de slides (30 minutos) \+ demonstração de funcionalidades   
* Artefato: Código-fonte compartilhado com a turma  
* Artefato: processo de migração fornecido junto com o deploy (create tables, carga inicial de dados, se necessário)  
* Deploy na camada free da Google Cloud ou Amazon AWS  
  * [https\://cloud.google.com/free](https://cloud.google.com/free)  
  * [https\://aws.amazon.com/pt/free/](https://aws.amazon.com/pt/free/)   
  * outra…

**Requisitos obrigatórios**

* Grupo com três ou quatro integrantes  
* Número **mínimo** de modelos (tabelas): de sete a dez \[ pode haver mais \]   
* [Customização do Admin](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/) (*fieldsets*, modelos *inline* etc)  
* Aplicação de recursos de [autenticação](https://docs.djangoproject.com/en/3.1/topics/auth/)   
  * Implementar recuperação de senha  
  * Utilizar recursos de envio de [e-mail](https://docs.djangoproject.com/en/3.1/topics/email/)   
* Aplicar recursos de [Validação de Dados](https://docs.djangoproject.com/en/3.1/ref/validators/)   
* Utilização de [banco de dados](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-DATABASES)  
  * Sugestões: Maria DB, Postgres, MySQL  
* Utilizar recursos:  
  * [*Humanização*](https://docs.djangoproject.com/en/3.1/ref/contrib/humanize/)  
  * [*Framework de Mensagens*](https://docs.djangoproject.com/en/3.1/ref/contrib/messages/)  
  * [*Paginação*](%20https://docs.djangoproject.com/en/3.1/topics/pagination/)   
* Definir um projeto (site) com, pelo menos duas aplicações (módulos) / [ver projetos vs. aplicações](https://docs.djangoproject.com/pt-br/3.1/ref/applications/)

**Requisitos desejáveis**

* [Sessões anônimas](https://docs.djangoproject.com/en/3.1/topics/http/sessions/)   
* Consumir dados de qualquer serviço online via API REST (ou similar):  
  * Clima  
  * Cotação de moedas e demais serviços financeiros  
  * Dados de governo  
  * Etc  
* Fornecer API para consumo de recursos por outros sistemas ou projetos dos colegas (é o inverso do item anterior, onde o seu projeto atuará como *server* e não como *client*)  
* Utilizar [internacionalização](https://docs.djangoproject.com/en/3.1/topics/i18n/) (inglês/português)

## Algumas referências úteis

* [Django Template Language](https://docs.djangoproject.com/en/3.1/topics/templates/#the-django-template-language)  
* [Autenticação de Usuários](https://docs.djangoproject.com/en/3.1/topics/auth/)  
* [Configurações do Django](https://docs.djangoproject.com/en/3.1/topics/settings/%20)  
* [Django Utils](https://docs.djangoproject.com/en/3.1/ref/utils/)   
* Proteção contra [falsificação de solicitação entre sites](https://docs.djangoproject.com/pt-br/3.1/ref/csrf/)  
* [Como customizar campos no MODEL](https://docs.djangoproject.com/en/3.1/howto/custom-model-fields/)  
* [Trabalhando com PDFs em Django](https://docs.djangoproject.com/en/3.1/howto/outputting-pdf/)  
* [Django Shortcuts](https://docs.djangoproject.com/en/3.1/topics/http/shortcuts/) (render, redirect, get\_object\_or\_404, etc)