#!/bin/bash
# ==============================================================================
# Automated Database & Media Backup Script for Nehru Place IT Services
# Recommended Cron Entry (Daily at 2:00 AM):
# 0 2 * * * /var/www/ecomnpits/backup.sh >> /var/log/ecomnpits_backup.log 2>&1
# ==============================================================================

set -e

ENV_FILE="/var/www/ecomnpits/.env"

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' $ENV_FILE | xargs)
fi

DB_NAME="${DB_NAME:-ecom_npits}"
DB_USER="${DB_USER:-ecom_npits}"
DB_PASS="${DB_PASSWORD:-ecom_npits_pass123}"
DB_HOST="${DB_HOST:-localhost}"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/backups/ecomnpits"
mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting backup for database '$DB_NAME'..."

# 1. MySQL Dump with gzip compression
mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" | gzip > "$BACKUP_DIR/db_${DB_NAME}_${TIMESTAMP}.sql.gz"

# 2. Compress Media directory
if [ -d "/var/www/ecomnpits/media" ]; then
    tar -czf "$BACKUP_DIR/media_${TIMESTAMP}.tar.gz" -C /var/www/ecomnpits media
fi

# 3. Retain last 30 days backups
find "$BACKUP_DIR" -type f -mtime +30 -delete

echo "[$(date)] Backup completed successfully: $BACKUP_DIR/db_${DB_NAME}_${TIMESTAMP}.sql.gz"
