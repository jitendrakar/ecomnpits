#!/bin/bash
# ==============================================================================
# Smart Incremental Deployment Script for Nehru Place IT Services VPS
# Performs fast, non-destructive sync of modified files only without re-seeding
# Repository: https://github.com/jitendrakar/ecomnpits.git
# Target Directory: /home/ecomnpits
# ==============================================================================

set -e

GIT_DIR="/home/ecomnpits_git"
APP_DIR="/home/ecomnpits"
REPO_URL="https://github.com/jitendrakar/ecomnpits.git"
FORCE_SEED=false

if [ "$1" == "--seed" ]; then
    FORCE_SEED=true
fi

echo "======================================================"
echo " Starting Smart Incremental VPS Deployment"
echo " Git Directory:   $GIT_DIR"
echo " App Directory:   $APP_DIR"
echo " Force Seeding:   $FORCE_SEED"
echo "======================================================"

# 1. Fetch latest changes from GitHub into $GIT_DIR
echo "[1/6] Fetching updated commits from GitHub..."
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

# 2. Incremental Sync (Only modified/changed code files updated)
echo "[2/6] Syncing modified files into $APP_DIR (preserving .env, venv, sqlite3 & media)..."
sudo mkdir -p "$APP_DIR"

if command -v rsync &> /dev/null; then
    sudo rsync -av --update \
        --exclude='.env' \
        --exclude='.env.backup' \
        --exclude='venv/' \
        --exclude='env/' \
        --exclude='*.sqlite3' \
        --exclude='media/' \
        --exclude='.git/' \
        "$GIT_DIR/" "$APP_DIR/"
else
    sudo cp -ru "$GIT_DIR"/* "$APP_DIR"/
fi

cd "$APP_DIR"

# Ensure .env exists
if [ ! -f "$APP_DIR/.env" ]; then
    if [ -f "$APP_DIR/.env.example" ]; then
        echo "Initializing .env from .env.example..."
        sudo cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    fi
fi

# 3. Virtual Environment & Requirements
echo "[3/6] Activating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 4. Apply Pending Database Migrations
echo "[4/6] Checking and applying database migrations..."
python manage.py migrate --noinput

# 5. Conditional Seeding (ONLY when database has 0 products or --seed flag is passed)
if [ "$FORCE_SEED" = true ]; then
    echo "[5/6] Force seeding database as requested (--seed)..."
    python manage.py seed_data
else
    PRODUCT_COUNT=$(python manage.py shell -c "from products.models import Product; print(Product.objects.count())" 2>/dev/null || echo "0")
    if [ "$PRODUCT_COUNT" -eq "0" ]; then
        echo "[5/6] Database is empty. Seeding initial products & categories..."
        python manage.py seed_data
    else
        echo "[5/6] Existing database contains $PRODUCT_COUNT products. Skipping seed_data to preserve custom data & price changes."
    fi
fi

# 6. Collect Static Assets & Fix Permissions
echo "[6/6] Collecting static assets & reloading services..."
python manage.py collectstatic --noinput
sudo mkdir -p media static_collected /var/log/gunicorn
sudo chmod 755 /home /home/ecomnpits /home/ecomnpits_git 2>/dev/null || true
sudo chmod -R 755 static_collected media "$APP_DIR"
sudo chown -R www-data:www-data media static_collected /var/log/gunicorn "$APP_DIR"

# Reload Nginx and Systemd App Service
if [ -f "nginx_nehruplaceitservices.conf" ]; then
    sudo cp nginx_nehruplaceitservices.conf /etc/nginx/sites-available/nehruplaceitservices.conf
    sudo ln -sf /etc/nginx/sites-available/nehruplaceitservices.conf /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx 2>/dev/null || sudo systemctl restart nginx
fi

if [ -f "ecomnpits.service" ]; then
    sudo cp ecomnpits.service /etc/systemd/system/ecomnpits.service
    sudo systemctl daemon-reload
    sudo systemctl enable ecomnpits 2>/dev/null || true
fi

sudo systemctl reload ecomnpits 2>/dev/null || sudo systemctl restart ecomnpits

echo "======================================================"
echo " INCREMENTAL DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo " Only modified files were updated. Existing DB & media preserved."
echo " Live Site: https://nehruplaceitservices.com/"
echo "======================================================"
