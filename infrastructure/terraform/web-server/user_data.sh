#!/bin/bash

# Script de inicialização para servidor web
# Executado automaticamente na primeira inicialização da instância

set -e

# Atualizar sistema
apt-get update
apt-get upgrade -y

# Instalar dependências básicas
apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    htop \
    tree \
    jq \
    awscli

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Instalar Nginx
apt-get install -y nginx

# Configurar Nginx básico
cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files \$uri \$uri/ =404;
    }

    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Criar página inicial personalizada
cat > /var/www/html/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>ByteShift Orchestrator - ${project_name}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            color: white;
            margin: 0;
            padding: 40px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        h1 {
            color: #3b82f6;
            margin-bottom: 20px;
        }
        .status {
            background: #10b981;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            margin: 20px 0;
        }
        .info {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 ByteShift Orchestrator</h1>
        <h2>Projeto: ${project_name}</h2>
        <div class="status">✅ Servidor Online</div>
        <div class="info">
            <p><strong>Hostname:</strong> $(hostname)</p>
            <p><strong>Deployed:</strong> $(date)</p>
            <p><strong>Managed by:</strong> ByteShift Orchestrator</p>
        </div>
        <p>Este servidor foi provisionado automaticamente pelo agente de IA.</p>
    </div>
</body>
</html>
EOF

# Iniciar e habilitar Nginx
systemctl start nginx
systemctl enable nginx

# Configurar firewall básico
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable

# Instalar agente de monitoramento (Node Exporter)
cd /tmp
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
cp node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
rm -rf node_exporter-1.6.1.linux-amd64*

# Criar serviço do Node Exporter
cat > /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=nobody
Group=nogroup
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# Iniciar Node Exporter
systemctl daemon-reload
systemctl start node_exporter
systemctl enable node_exporter

# Log de conclusão
echo "$(date): Servidor web configurado com sucesso" >> /var/log/user-data.log

# Sinalizar conclusão
/opt/aws/bin/cfn-signal -e $? --stack ${project_name} --resource WebServerInstance --region $(curl -s http://169.254.169.254/latest/meta-data/placement/region) || true
