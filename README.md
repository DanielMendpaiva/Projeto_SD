# Projeto RotaAlt - Sistemas Distribuídos (SD)

Sistema web desenvolvido em Django para gestão de transporte alternativo, linhas, veículos, reservas e passageiros.

---

## 🛠️ Pré-requisitos na Máquina Física (Host)

Antes de começar, certifique-se de ter instalado no seu computador:
1. **[VirtualBox](https://www.virtualbox.org/)** (gerenciador de máquinas virtuais)
2. **[Vagrant](https://developer.hashicorp.com/vagrant/install)** (ferramenta para automação da VM)
3. **[Git](https://git-scm.com/)**

---

## 🚀 Como Iniciar o Projeto com Vagrant e Venv

Siga o passo a passo abaixo no terminal do seu computador (PowerShell ou Prompt de Comando):

### 1. Baixar o projeto
```bash
git clone <URL_DO_REPOSITORIO>
cd Projeto_SD
```

### 2. Iniciar a Máquina Virtual (VM)
Este comando baixa a imagem do Ubuntu e instala automaticamente o Python 3 e o SQLite:
```bash
vagrant up
```
*(Esse comando pode demorar alguns minutos apenas na primeira vez).*

### 3. Acessar o terminal da Máquina Virtual
```bash
vagrant ssh
```

---

## 💻 Dentro da Máquina Virtual (Terminal Linux)

Após entrar na VM via `vagrant ssh`, execute os seguintes comandos:

### 1. Entrar na pasta do projeto compartilhada
```bash
cd /vagrant
```

### 2. Criar e ativar o ambiente virtual (venv do Linux)
> **Dica:** Criamos o `venv` na pasta pessoal do usuário (`~/venv`) para garantir maior velocidade de execução no Linux:
```bash
# Cria o ambiente virtual
python3 -m venv ~/venv

# Ativa o ambiente virtual
source ~/venv/bin/activate
```
*(Você verá `(venv)` no início da linha do terminal).*

### 3. Instalar as bibliotecas do projeto
```bash
pip install -r requirements.txt
```

### 4. Preparar o banco de dados e dados de teste
```bash
# Aplica as tabelas no banco de dados SQLite
python manage.py migrate

# Popula o banco com usuários fictícios, rotas e cria o admin
python populate.py
```

### 5. Iniciar o servidor Django
> **Atenção:** É obrigatório usar `0.0.0.0:8000` para que a VM permita o acesso pelo navegador do seu Windows:
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🌐 Acessando a Aplicação no Navegador

Abra o navegador do seu computador e acesse:
* **Painel Administrativo:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
* **Usuário:** `admin`
* **Senha:** `admin123`

---

## 📌 Comandos Úteis do Dia a Dia (no seu computador)

Quando terminar de estudar ou trabalhar no projeto:

* **Parar o servidor Django:** Pressione `Ctrl + C` no terminal da VM.
* **Sair do terminal da VM:** Digite `exit`.
* **Desligar a Máquina Virtual:** `vagrant halt`
* **Ligar a VM novamente no dia seguinte:** `vagrant up`
* **Destruir a VM para recriar do zero (se der algum problema):** `vagrant destroy -f` e depois `vagrant up`

---

## 🗄️ Sobre as Tabelas do Banco de Dados

Ao executar as migrações com `python manage.py migrate`, o Django gera ao todo **20 tabelas** no banco de dados SQLite (`db.sqlite3`), distribuídas entre tabelas de negócio do projeto e tabelas de infraestrutura nativa do framework:

### 1. Tabelas de Negócio do RotaAlt (10 tabelas)

Criadas a partir dos modelos (`models.py`) implementados para as regras do sistema:

#### 👤 App `contas` (1 tabela)
* **`contas_perfil`** (`Perfil`): Estende o usuário padrão do Django adicionando tipo de acesso (`passageiro`, `motorista` ou `gestor`), CPF, telefone e data de nascimento.

#### 🚐 App `transporte` (7 tabelas)
* **`transporte_operador`** (`Operador`): Cooperativas e empresas operadoras de transporte alternativo (nome, CNPJ, e-mail, telefone e endereço).
* **`transporte_veiculo`** (`Veiculo`): Frota de veículos cadastrados (placa, modelo, tipo de veículo como van ou micro-ônibus, capacidade de passageiros e ano).
* **`transporte_motorista`** (`Motorista`): Motoristas vinculados a um operador e ao seu perfil de usuário, contendo número e categoria da CNH.
* **`transporte_parada`** (`Parada`): Pontos de embarque e desembarque com endereço e coordenadas geográficas (latitude e longitude).
* **`transporte_rota`** (`Rota`): Linhas e itinerários atendidos pelos operadores.
* **`transporte_paradarota`** (`ParadaRota`): Tabela intermediária (*through*) que define a ordem sequencial das paradas em cada rota e o tempo estimado de deslocamento entre elas.
* **`transporte_viagem`** (`Viagem`): Viagens agendadas, em andamento ou concluídas, vinculando rota, veículo, motorista, horários de saída/chegada, vagas disponíveis, tarifa e status.

#### 🎫 App `reservas` (2 tabelas)
* **`reservas_reserva`** (`Reserva`): Controle das reservas de passagens e vagas feitas por passageiros para viagens específicas.
* **`reservas_avaliacao`** (`Avaliacao`): Avaliações e notas (1 a 5) com comentários deixados pelos passageiros após a viagem.

---

### 2. Tabelas Nativas do Django (10 tabelas)

Criadas automaticamente para suporte à infraestrutura, segurança e painel do Django:

* **Autenticação e Permissões (`django.contrib.auth`)**:
  * **`auth_user`**: Cadastro de usuários do sistema (administradores, passageiros e operadores).
  * **`auth_group`**: Grupos de permissões de acesso.
  * **`auth_permission`**: Permissões individuais de CRUD para cada modelo do banco.
  * **`auth_user_groups`**: Associação entre usuários e seus grupos.
  * **`auth_user_user_permissions`**: Permissões específicas concedidas diretamente a um usuário.
  * **`auth_group_permissions`**: Permissões associadas a cada grupo.
* **Painel Administrativo (`django.contrib.admin`)**:
  * **`django_admin_log`**: Histórico e auditoria de ações realizadas dentro do `/admin/`.
* **Sessões (`django.contrib.sessions`)**:
  * **`django_session`**: Armazenamento de sessões de login e cookies de autenticação no navegador.
* **Tipos de Conteúdo (`django.contrib.contenttypes`)**:
  * **`django_content_type`**: Mapeamento e catálogo interno de todos os modelos registrados.
* **Controle de Migrações (`django.db.migrations`)**:
  * **`django_migrations`**: Registro do histórico e status de cada migração executada no banco.