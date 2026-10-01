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