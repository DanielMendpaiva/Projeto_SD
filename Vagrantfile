# -*- mode: ruby -*-
# vi: set ft=ruby :

# Configuracao da Maquina Virtual para o Projeto_SD
Vagrant.configure("2") do |config|

  # 1. Sistema Operacional da VM
  config.vm.box = "ubuntu/jammy64"

  # 2. Redirecionamento de Portas
  # O servidor do Django rodando na porta 8000 na VM.
  # Para abrir no navegador do Windows em http://localhost:8000
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # 3. Configuracoes de Recursos no VirtualBox
  config.vm.provider "virtualbox" do |vb|
    vb.name = "projeto_sd_vm" # Nome que aparece no VirtualBox
    vb.memory = "2048"        # Quantidade de memoria RAM
    vb.cpus = 2               # Quantidade de processadores virtuais
  end

  # 4. Instalacao automatica na primeira vez que a VM ligar (Provisionamento)
  # Instala o Python 3, o pip, a ferramenta de venv e o SQLite dentro do Linux
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    
    echo "=== Atualizando lista de pacotes do Ubuntu ==="
    apt-get update -y

    echo "=== Instalando Python 3, pip, venv e SQLite ==="
    apt-get install -y python3 python3-pip python3-venv sqlite3 build-essential

    echo "=== Instalacao concluida! ==="
  SHELL
end
