# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Box padrão recomendada: Ubuntu 22.04 LTS
  config.vm.box = "ubuntu/jammy64"

  # Redirecionamento da porta do Django (8000 da VM -> 8000 da máquina host)
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Configurações de recursos da VM (VirtualBox)
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
    vb.name = "projeto_sd_vm"
  end

  # Script de provisionamento automático na criação da VM
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    echo "=== Atualizando pacotes do sistema ==="
    apt-get update -y
    apt-get install -y python3 python3-pip python3-venv sqlite3 build-essential

    echo "=== Provisionamento concluído com sucesso! ==="
  SHELL
end
