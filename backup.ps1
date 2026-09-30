# Windows PowerShell backup script for ecom_npits MySQL database

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupDir = "G:\My Drive\NETPROFIT\ecomnpits\backups"
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

$MySQLDump = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
$OutputFile = "$BackupDir\ecom_npits_$Timestamp.sql"

& $MySQLDump -u ecom_npits -pecom_npits_pass123 ecom_npits > $OutputFile

Write-Host "Database ecom_npits backed up successfully to: $OutputFile"
