#!/bin/bash
# ==============================================================================
# Automated Staged Deployment Script for Nehru Place IT Services VPS
# Workflow: Clones/pulls GitHub repo into /home/ecomnpits_git and syncs to /home/ecomnpits
# Repository: https://github.com/jitendrakar/ecomnpits.git
# Target Directory: /home/ecomnpits
# Port: 127.0.0.1:8001
# ==============================================================================

set -e

GIT_DIR="/home/ecomnpits_git"
APP_DIR="/home/ecomnpits"
REPO_URL="https://github.com/jitendrakar/ecomnpits.git"

echo "======================================================"
echo " Starting Staged VPS Deployment"
echo " Git Staging Directory: $GIT_DIR"
echo " Target App Directory:  $APP_DIR"
echo "======================================================"

# 1. Fetch / Clone latest code into /home/ecomnpits_git
echo "[1/7] Fetching latest code from GitHub into $GIT_DIR..."
if [ -d "$GIT_DIR/.git" ]; then
    cd "$GIT_DIR"
    git remote set-url origin "$REPO_URL" 2>/dev/null || true
    git fetch origin main
    git reset --hard origin/main
else
    sudo rm -rf "$GIT_DIR"
    git clone "$REPO_URL" "$GIT_DIR"
    cd "$GIT_DIR"
fi

# 2. Copy/Sync updated codebase to /home/ecomnpits (Preserves existing .env and venv)
echo "[2/7] Copying updated files to $APP_DIR..."
sudo mkdir -p "$APP_DIR"
sudo cp -r "$GIT_DIR"/* "$APP_DIR"/

cd "$APP_DIR"

# Ensure .env exists in target app directory
if [ ! -f "$APP_DIR/.env" ]; then
    if [ -f "$APP_DIR/.env.example" ]; then
        echo "Initializing default .env from .env.example..."
        sudo cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    fi
fi

# 3. Virtual Environment Setup & Dependencies
echo "[3/7] Checking Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Apply Database Migrations
echo "[4/7] Applying database migrations..."
python manage.py migrate --noinput

# 5. Seed Products, Categories, Services, CCTV Rates & Admin Superuser (admin / admin123)
echo "[5/7] Seeding products, services, CCTV pricing, and admin superuser..."
python manage.py seed_data

# 6. Collect Static Assets & Fix Permissions
echo "[6/7] Collecting static assets & fixing directory permissions..."
python manage.py collectstatic --noinput
sudo mkdir -p media static_collected /var/log/gunicorn
sudo chmod 755 /home /home/ecomnpits /home/ecomnpits_git 2>/dev/null || true
sudo chmod -R 755 static_collected media "$APP_DIR"
sudo chown -R www-data:www-data media static_collected /var/log/gunicorn "$APP_DIR"


# 7. Configure Nginx and Systemd Daemon
echo "[7/7] Configuring Nginx reverse proxy (127.0.0.1:8001) & reloading services..."

# Clean up any old conflicting Nginx site symlinks for nehruplaceitservices.com
for old_conf in /etc/nginx/sites-enabled/*; do
    if [ "$old_conf" != "/etc/nginx/sites-enabled/nehruplaceitservices.conf" ]; then
        if grep -qs "nehruplaceitservices.com" "$old_conf"; then
            echo "Removing conflicting Nginx config: $old_conf"
            sudo rm -f "$old_conf"
        fi
    fi
done

if [ -f "nginx_nehruplaceitservices.conf" ]; then
    sudo cp nginx_nehruplaceitservices.conf /etc/nginx/sites-available/nehruplaceitservices.conf
    sudo ln -sf /etc/nginx/sites-available/nehruplaceitservices.conf /etc/nginx/sites-enabled/
    sudo nginx -t
fi


# Clean up any old systemd override files that cause conflicts
sudo rm -rf /etc/systemd/system/ecomnpits.service.d

if [ -f "ecomnpits.service" ]; then
    sudo cp ecomnpits.service /etc/systemd/system/ecomnpits.service
    sudo systemctl unmask ecomnpits 2>/dev/null || true
    sudo systemctl daemon-reload
    sudo systemctl enable ecomnpits 2>/dev/null || true
fi

sudo systemctl restart ecomnpits
sudo systemctl reload nginx 2>/dev/null || sudo systemctl restart nginx

echo "======================================================"
echo " DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo " Live Website:   https://nehruplaceitservices.com/"
echo " Admin Panel:    https://nehruplaceitservices.com/admin/"
echo " Admin Login:    User 'admin' | Password 'admin123'"
echo "======================================================"
