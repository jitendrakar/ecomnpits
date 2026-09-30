# NEHRU PLACE IT SERVICES

## Complete E-Commerce & IT Services Platform

**Domain:** `nehruplaceitservices.com`  
**Stack:** Python 3.12+ / Django 5.x / MySQL 8.x / Gunicorn / Nginx / Docker  
**Database:** `ecom_npits` | **User:** `ecom_npits` | **Host:** `localhost`  
**Design Theme:** Modern AI/IT Visual System (Dark Navy `#050B14`, Cyan Glow `#00E5FF`, Purple Glow `#7C3AED`)

---

## 1. Features Overview

1. **Database-Driven Architecture**: All products, prices, service packages, CCTV rates, warranty terms, marketplaces, testimonials, and contact information are managed dynamically via Django Admin without hardcoded HTML.
2. **Product Catalog & External Marketplace Purchasing**:
   - Product categories, brands, specifications, stock status, and multiple images.
   - External marketplace purchase buttons (**Amazon, Flipkart, Meesho**) with click tracking analytics (`MarketplaceClick`).
   - Advanced search (name, SKU, category, brand, description), multi-field filtering, and sorting.
3. **IT Services Platform**:
   - Dynamic service packages (Basic, Standard, Premium) for Website Development, CCTV Installation, Office Networking, Computer Repair, and IT Support.
4. **Live CCTV Quotation Calculator**:
   - URL: `/services/cctv-calculator/`
   - Real-time client calculation powered by MySQL `CCTVPricing` model (cameras, DVR/NVR, HDD, power supply, connectors, cable meter cost, installation labor, wiring labor, and maintenance AMC).
   - "Request Detailed Quote" form saving exact cost breakdowns into `Enquiry.calculation_details`.
5. **Enquiry & Lead Management System**:
   - Stores leads from General Website, Product Pages, Service Pages, CCTV Calculator, Contact Page, and WhatsApp links.
   - Admin search, filtering, status tracking (`NEW`, `CONTACTED`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`), and email notifications.
6. **WhatsApp Integration**:
   - Configurable WhatsApp number from `SiteSettings` with pre-filled pre-formatted URL encoding.
7. **Branded Django Admin Dashboard**:
   - Custom Header & Dashboard metrics (Total/Active Products, Services, New/Pending Enquiries, Recent Lead tables).
8. **SEO & Security Ready**:
   - Automatic `sitemap.xml` and `robots.txt` generation.
   - Custom 404, 403, and 500 pages matching AI/IT design system.
   - Uptime monitoring endpoint `/health/`.
   - Environment secret separation (`.env`), WhiteNoise static file handling, SSL header proxy detection, and HTTPS readiness.

---

## 2. Environment Setup & Local Running

### Prerequisites
- Python 3.12+
- MySQL 8.x Server (Running on `localhost:3306`)

### Installation Steps

1. **Navigate to Project Directory**:
   ```bash
   cd "G:\My Drive\NETPROFIT\ecomnpits"
   ```

2. **Environment File (`.env`) Configuration**:
   Ensure `.env` exists in project root:
   ```env
   DEBUG=True
   SECRET_KEY=django-insecure-npits-key-83749281749817293817298371928371
   ALLOWED_HOSTS=localhost,127.0.0.1,nehruplaceitservices.com,www.nehruplaceitservices.com

   DB_NAME=ecom_npits
   DB_USER=ecom_npits
   DB_PASSWORD=ecom_npits_pass123
   DB_HOST=localhost
   DB_PORT=3306
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**:
   ```bash
   python manage.py makemigrations core products services enquiries
   python manage.py migrate
   ```

5. **Populate Initial Seed Data**:
   ```bash
   python manage.py seed_data
   ```

6. **Create Admin User** (or use default `admin`/`admin123`):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open browser at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
   Admin Panel at: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 3. Project Directory Structure

```
ecomnpits/
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── Dockerfile              # Docker container setup
├── docker-compose.yml      # Orchestrated setup (MySQL + Django + Nginx)
├── setup_vps.sh            # Automated 1-click installer for Ubuntu/Debian VPS
├── deploy.sh               # Quick deploy script for VPS
├── gunicorn.conf.py        # Production Gunicorn configuration
├── nginx_nehruplaceitservices.conf # Production Nginx reverse proxy with SSL
├── ecomnpits.service       # Systemd daemon configuration
├── backup.sh / backup.ps1  # Automated MySQL & Media backups
├── config/                 # Root Django Project Settings & Routing
├── core/                   # SiteSettings, Testimonials, CMS Pages, Health Check & Seed Command
├── products/               # Categories, Brands, Products, Specs, Marketplace Links & Click Analytics
├── services/               # Categories, Services, Features, Packages & CCTV Pricing Engine
├── enquiries/              # Lead Models, Status Management & Enquiry Forms
├── templates/              # Responsive HTML5 Templates with AI/IT Styling
├── static/                 # CSS (style.css), JS (main.js), Images
└── media/                  # Uploaded Product Images, Banners & Attachments
```

---

## 4. Production VPS Deployment Guide

You can deploy the project to any Linux VPS (Ubuntu 22.04 / 24.04 LTS recommended) using either **Automated Script**, **Native Systemd + Nginx**, or **Docker Compose**.

### Option A: 1-Click Automated VPS Setup (Recommended)

Run the included automated setup script directly on your fresh Ubuntu VPS:

```bash
chmod +x setup_vps.sh
sudo ./setup_vps.sh
```

This script automatically:
1. Installs Python 3.12, MySQL 8, Nginx, Certbot, UFW firewall.
2. Creates MySQL database `ecom_npits` and secure user.
3. Sets up virtual environment and installs Python packages.
4. Generates production `.env` file with secure random secret keys.
5. Performs database migrations, seeds initial data, and collects static assets.
6. Configures systemd daemon (`ecomnpits.service`).
7. Issues SSL Certificate via Let's Encrypt and enables HTTPS on Nginx.

---

### Option B: Native Systemd + Nginx + Gunicorn (Manual)

1. **Transfer Codebase to VPS**:
   ```bash
   sudo mkdir -p /var/www/ecomnpits
   sudo chown -R $USER:www-data /var/www/ecomnpits
   # Copy or git clone files into /var/www/ecomnpits
   ```

2. **Configure Production `.env`**:
   ```bash
   cp .env.example .env
   nano .env
   ```
   *Set `DEBUG=False`, update `SECRET_KEY`, and set your production MySQL credentials.*

3. **Virtual Environment & Static Assets**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_data
   python manage.py collectstatic --noinput
   ```

4. **Setup Systemd Daemon**:
   ```bash
   sudo cp ecomnpits.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now ecomnpits
   ```

5. **Setup Nginx & SSL Certificate**:
   ```bash
   sudo cp nginx_nehruplaceitservices.conf /etc/nginx/sites-available/nehruplaceitservices.conf
   sudo ln -sf /etc/nginx/sites-available/nehruplaceitservices.conf /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo certbot --nginx -d nehruplaceitservices.com -d www.nehruplaceitservices.com
   sudo systemctl reload nginx
   ```

---

### Option C: Docker Compose Deployment

If you prefer containerized deployment:

1. **Install Docker & Docker Compose on VPS**:
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```

2. **Start Services**:
   ```bash
   cp .env.example .env
   # Edit .env with your domain and settings
   docker compose up -d --build
   ```

3. **Check Container Status**:
   ```bash
   docker compose ps
   docker compose logs -f web
   ```

---

## 5. Ongoing Updates & Deployment (`deploy.sh`)

To push updates to your live VPS, run:

```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 6. Maintenance & Automated Backups

- **Automated Linux Daily Cron Backup**:
  Add to crontab (`crontab -e`):
  ```cron
  0 2 * * * /var/www/ecomnpits/backup.sh >> /var/log/ecomnpits_backup.log 2>&1
  ```

- **Manual Backups**:
  - **Linux**: `./backup.sh` (Saves compressed MySQL dump and media files to `/var/backups/ecomnpits`).
  - **Windows**: `.\backup.ps1`

---

## 7. Troubleshooting & Verification

- **Check App Status**: `sudo systemctl status ecomnpits`
- **View Live Logs**: `journalctl -u ecomnpits -f` or `tail -f django_error.log`
- **Test Health Endpoint**: `curl http://127.0.0.1:8000/health/` -> Output: `OK`
