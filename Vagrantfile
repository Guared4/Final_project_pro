Vagrant.configure("2") do |config|
  nodes = [
    { name: "frontend",  ip: "192.168.57.10", ip_ext: "192.168.57.100", cpus: 2, memory: 2048 },
    { name: "backend1",  ip: "192.168.57.11", cpus: 2, memory: 2048 },
    { name: "backend2",  ip: "192.168.57.12", cpus: 2, memory: 2048 },
    { name: "db-master", ip: "192.168.57.13", cpus: 2, memory: 1024 },
    { name: "db-slave",  ip: "192.168.57.14", cpus: 2, memory: 1024 },
    { name: "monitoring", ip: "192.168.57.15", cpus: 4, memory: 6144 },
    { name: "backup",    ip: "192.168.57.16", cpus: 1, memory: 1024 }
  ]

  nodes.each do |node|
    config.vm.define node[:name] do |node_config|
      node_config.vm.box = "ubuntu/jammy64"
      node_config.vm.hostname = node[:name]
      node_config.vm.network "private_network", ip: node[:ip]
      
      # Добавляем второй IP только для frontend
      if node[:name] == "frontend"
        node_config.vm.network "private_network", ip: node[:ip_ext], virtualbox__intnet: true
      end

      node_config.vm.provider "virtualbox" do |vb|
        vb.memory = node[:memory]
        vb.cpus = node[:cpus]
      end

      ssh_pub_key = File.readlines("./id_rsa/id_rsa.pub").first.strip
      node_config.vm.provision "shell", inline: <<-SHELL
        echo #{ssh_pub_key} >> ~vagrant/.ssh/authorized_keys
        echo #{ssh_pub_key} >> ~root/.ssh/authorized_keys
        sudo sed -i 's/#PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
        sudo systemctl restart sshd
      SHELL
    end
  end
end