# Setup Guide

This guide explains how to use the setup script to customize the Autobots for your project.

## Quick Start

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Follow the prompts:**
   - **App Display Name**: The human-readable name (e.g., "My Awesome App")
   - **Project Name**: Kebab-case name for Docker images, buckets (e.g., "my-awesome-app")
   - **Snake Case Name**: For database and package names (e.g., "my_awesome_app")
   - **Database Name**: PostgreSQL database name (defaults to snake case name)
   - **S3 Bucket Name**: Storage bucket name (defaults to project name)
   - **Docker Image Prefix**: Prefix for Docker images (defaults to project name)
   - **Log File Prefix**: Prefix for log files (defaults to snake case name)

## Example Session

```
🚀 Welcome to Autobots Setup!
==================================================
This script will help you customize the template for your project.
Please provide the following information:

📱 App Display Name (e.g., 'My Awesome App'): TaskMaster Pro
📦 Project Name (kebab-case, e.g., 'my-awesome-app'): taskmaster-pro
🐍 Snake Case Name (for database/package, default: 'taskmaster_pro'): taskmaster_pro
🗄️  Database Name (default: 'taskmaster_pro'): taskmaster_pro
🪣 S3 Bucket Name (default: 'taskmaster-pro'): taskmaster-pro-storage
🐳 Docker Image Prefix (default: 'taskmaster-pro'): taskmaster-pro
📝 Log File Prefix (default: 'taskmaster_pro'): taskmaster_pro

==================================================
📋 Configuration Summary
==================================================
Display Name:     'TaskMaster Pro'
Project Name:     'taskmaster-pro'
Package Name:     'taskmaster_pro'
Database Name:    'taskmaster_pro'
Bucket Name:      'taskmaster-pro-storage'
Docker Prefix:    'taskmaster-pro'
Log Prefix:       'taskmaster_pro'

🔄 The following replacements will be made:
  'Autobots' → 'TaskMaster Pro'
  'app-template' → 'taskmaster-pro'
  'app_template' → 'taskmaster_pro'
  Database: 'app_template' → 'taskmaster_pro'
  Bucket: 'app-template' → 'taskmaster-pro-storage'
  Docker images: 'app-template-*' → 'taskmaster-pro-*'
  Log files: 'app_template_*' → 'taskmaster_pro_*'

📁 Files to be modified: 12

✅ Proceed with these changes? (y/N): y
```

## What Gets Changed

### Display Names
- `web/app/layouts/default.vue` - Page title
- `web/app/components/auth/Login.vue` - Welcome message
- `web/app/pages/home.vue` - Page heading
- `web/app/app.vue` - Meta tags and titles
- `README.md` - Project title

### Project Configuration
- `package.json` - Root package name
- `docker-compose.dev.yml` - Service names, database name, bucket names
- `postgres/init/01-create_database.sql` - Database creation
- `backend/config/settings.py` - Log file paths
- `web/build.sh` - Docker image names

### Docker & Infrastructure
- All Docker image names (backend, web)
- MinIO bucket configurations
- Environment variable defaults
- Log file paths

## Backup & Recovery

The script automatically creates a backup in `backup_original/` before making changes. If something goes wrong:

1. **Restore from backup:**
   ```bash
   # Stop any running services
   docker-compose -f docker-compose.dev.yml down

   # Restore files
   cp -r backup_original/* .

   # Restart services
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Clean up backup when satisfied:**
   ```bash
   rm -rf backup_original/
   ```

## Manual Verification

After running the setup script, verify the changes:

1. **Check package.json:**
   ```bash
   grep -n "name" package.json
   ```

2. **Check Docker compose:**
   ```bash
   grep -n "image:" docker-compose.dev.yml
   ```

3. **Check database config:**
   ```bash
   grep -n "DB_NAME" docker-compose.dev.yml
   ```

4. **Test the application:**
   ```bash
   pnpm run infra:dev:up
   ```

## Troubleshooting

### Script fails with permission error
```bash
chmod +x setup.sh
chmod +x setup.py
```

### Python not found
Make sure Python 3 is installed:
```bash
python3 --version
```

### Backup directory already exists
The script will automatically remove and recreate the backup directory.

### Want to run setup again
1. Restore from backup first
2. Run the setup script again with new values

## Environment Variables

After running the setup script, update your `.env` files with the new values:

```env
# Example .env file
DB_NAME=your_new_database_name
AWS_STORAGE_BUCKET_NAME=your-new-bucket-name
```

Check `docker-compose.dev.yml` for all environment variables that may need updating.
