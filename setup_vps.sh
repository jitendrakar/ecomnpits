#!/bin/bash
# ==============================================================================
# Automated Safe VPS Installer Script for Nehru Place IT Services
# Multi-Site Coexistence: SAFELY installs without touching existing websites,
# existing databases, existing Nginx configs, or existing ports.
# Compatible OS: Ubuntu 22.04 LTS / 24.04 LTS / Debian 12
# ==============================================================================

set -e

DOMAIN="nehruplaceitservices.com"
WWW_DOMAIN="www.nehruplaceitservices.com"
APP_DIR="/var/www/ecomnpits"
APP_PORT="8002"
DB_NAME="ecom_npits"
DB_USER="ecom_npits"
DB_PASS=$(openssl rand -base64 16 | tr -dc 'a-zA-Z0-9' | head -c 16)
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))" 2>/dev/null || echo $(openssl rand -base64 32))

echo "======================================================"
echo " Starting Multi-Site Safe VPS Setup for $DOMAIN"
echo " Dedicated App Port: 127.0.0.1:$APP_PORT"
echo "======================================================"

# 1. Install required packages (Preserves existing packages)
echo "[1/8] Checking & installing system packages..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential \
                    default-libmysqlclient-dev pkg-config \
                    nginx certbot python3-certbot-nginx ufw curl git

# 2. Configure Firewall (UFW) without disrupting existing rules
echo "[2/8] Ensuring HTTP/HTTPS & SSH ports are open in UFW..."
sudo ufw allow OpenSSH || true
sudo ufw allow 'Nginx Full' || true
sudo ufw --force enable || true

# 3. Setup Dedicated MySQL Database (Does NOT touch existing databases)
echo "[3/8] Creating isolated MySQL database '$DB_NAME'..."
sudo systemctl start mysql || sudo systemctl start mariadb

sudo mysql -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
sudo mysql -e "GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

echo "Database '$DB_NAME' isolated successfully."

# 4. Prepare Dedicated App Directory (Isolated in /var/www/ecomnpits)
echo "[4/8] Setting up application directory at $APP_DIR..."
sudo mkdir -p $APP_DIR
sudo chown -R $USER:www-data $APP_DIR

if [ ! -f "$APP_DIR/manage.py" ]; then
    echo "Copying files to $APP_DIR..."
    cp -r ./* $APP_DIR/
fi

cd $APP_DIR

# 5. Virtual Environment & Dependencies
echo "[5/8] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create dedicated .env file
if [ ! -f "$APP_DIR/.env" ]; then
    echo "[Env Setup] Generating production .env file..."
    cat <<EOF > $APP_DIR/.env
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=$DOMAIN,$WWW_DOMAIN,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://$WWW_DOMAIN

GUNICORN_BIND=127.0.0.1:$APP_PORT

DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASS
DB_HOST=localhost
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@nehruplaceitservices.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=Nehru Place IT Services <info@nehruplaceitservices.com>
ADMIN_NOTIFICATION_EMAIL=admin@nehruplaceitservices.com
EOF
    echo ".env file generated successfully."
fi

# 6. Django Migrations & Collect Static
echo "[6/8] Running Django migrations and collecting static files..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_data

sudo chown -R www-data:www-data $APP_DIR/media $APP_DIR/static_collected
sudo chmod -R 775 $APP_DIR/media $APP_DIR/static_collected

# 7. Setup Systemd Service (Isolated unit ecomnpits.service)
echo "[7/8] Configuring Systemd service 'ecomnpits.service'..."
sudo cp $APP_DIR/ecomnpits.service /etc/systemd/system/ecomnpits.service
sudo systemctl daemon-reload
sudo systemctl enable ecomnpits
sudo systemctl restart ecomnpits

# 8. Setup Isolated Nginx Site (Does NOT delete or disturb any existing website configs)
echo "[8/8] Adding Nginx domain config for $DOMAIN..."
sudo cp $APP_DIR/nginx_nehruplaceitservices.conf /etc/nginx/sites-available/nehruplaceitservices.conf
sudo ln -sf /etc/nginx/sites-available/nehruplaceitservices.conf /etc/nginx/sites-enabled/

# Test Nginx syntax without breaking active sites
sudo nginx -t

# Request SSL Certificate specifically for this domain
echo "Requesting SSL certificate from Let's Encrypt for $DOMAIN..."
sudo certbot --nginx -d $DOMAIN -d $WWW_DOMAIN --non-interactive --agree-tos --register-unsafely-without-email || true

# Reload Nginx safely
sudo systemctl reload nginx

echo "======================================================"
echo " MULTI-SITE SAFE SETUP COMPLETED SUCCESSFULLY!"
echo "======================================================"
echo "Domain: https://$DOMAIN"
echo "Internal Port: 127.0.0.1:$APP_PORT"
echo "Database: $DB_NAME (User: $DB_USER)"
echo "Service Status: sudo systemctl status ecomnpits"
echo "Existing websites on this server were NOT modified."
echo "======================================================"
