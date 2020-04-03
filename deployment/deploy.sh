#!/bin/bash

BGM_NAME=${BGM_NAME:-BoardGameRooms}
BGM_PORT=${BGM_PORT:-5000}
BGM_GUNICORN=${BGM_GUNICORN:-boardgamerooms}


clear
echo "Settings:"
echo "========="
echo "domain:"
echo $DOMAIN
echo "Deploy Board Game Rooms? (y/n)"
read continue
if [[ $continue = "y" ]]
then
echo "Starting base installation"

echo "Updating system==============================="
cd
sudo apt -y update
sudo apt -y upgrade
echo "System updated================================"


echo "Installing install_base dependencies=================="
sudo apt -y install supervisor python3 python3-venv python3-dev mysql-server supervisor nginx git npm
echo "Base dependencies installed==================="


echo "Installing SSL certificate===================="
sudo apt install -y software-properties-common
sudo add-apt-repository -y universe
sudo add-apt-repository -y ppa:certbot/certbot
sudo apt install -y certbot python-certbot-nginx
sudo certbot certonly --nginx -d $DOMAIN
echo "Installing SSL certificate complete==========="


echo "Configuring firewall=========================="
sudo apt -y install ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw --force enable
echo "Configuring firewall complete================="


echo "Installing venv==============================="
python3 -m venv venv
source venv/bin/activate
pip install pip --upgrade
pip install setuptools --upgrade
pip install -r requirements.txt
pip install gunicorn
deactivate
echo "Installing venv complete======================"


echo "Building frontend============================="
npm install
npm run build
echo "Building frontend complete===================="


echo "Setting up supervisor========================="
sudo -E bash -c 'cat > /etc/supervisor/conf.d/$BGM_GUNICORN.conf' << EOL
[program:$BGM_NAME]
command=$HOME/$BGM_NAME/venv/bin/gunicorn -b 127.0.0.1:$BGM_PORT --worker-class eventlet -w 1 run:app
directory=$HOME/$BGM_NAME
user=$USER
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
EOL
sudo supervisorctl reload
echo "Setting up supervisor complete================"


echo "Setting up nginx for backend=================="
sudo -E bash -c 'cat > /etc/nginx/conf.d/$DOMAIN.conf' << EOL
server {
    listen 443 ssl http2;
    server_name $DOMAIN;

    location / {
        root $HOME/$BGM_NAME/dist;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:$BGM_PORT;
        include proxy_params;
        proxy_redirect off;
        proxy_buffering off;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /api/ping {
        include proxy_params;
        proxy_pass http://127.0.0.1:$BGM_PORT/api/ping;
    }

    access_log /var/log/$DOMAIN.access.log;
    error_log /var/log/$DOMAIN.error.log;
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    ssl_ecdh_curve secp521r1:secp384r1:prime256v1;
}
server {
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}
EOL
sudo service nginx reload
echo "Setting up nginx for backend complete========="


echo "Creating update script========================"
bash -c 'cat > deployment/update' << EOL
echo "Checking out new version===="
git pull
echo "========================Done"
echo "Installing requirements====="
source venv/bin/activate
pip install -r requirements.txt
echo "========================Done"
echo "Building frontend==========="
npm install
npm run build
echo "========================Done"
echo "Restarting Services========="
sudo supervisorctl restart $BGM_GUNICORN
sudo systemctl reload nginx
echo "========================Done"
EOL
echo "Created update script========================="


else
echo "Cancelling installation."
fi
