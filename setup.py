#!/usr/bin/env python3
"""
Setup script for App Template repository.
This script helps developers customize the template by replacing placeholder strings
with their own project-specific values.
"""

import os
import re
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


class ProjectSetup:
    def __init__(self):
        self.root_dir = Path(__file__).parent.absolute()
        self.replacements = {}
        
        # Define file patterns and their replacement contexts
        self.file_replacements = {
            # Display name replacements (App Template)
            'display_name': [
                'web/app/layouts/default.vue',
                'web/app/components/auth/Login.vue',
                'web/app/pages/home.vue',
                'web/app/app.vue',
                'web/app/pages/simple.vue',
                'scripts/init-db-user.sh',
                'README.md'
            ],
            # Kebab case replacements (app-template)
            'kebab_case': [
                'docker-compose.dev.yml',
                'web/build.sh',
                'README.md',
                '.env.example'
            ],
            # Snake case replacements (app_template)
            'snake_case': [
                'package.json',
                'postgres/init/01-create_database.sql',
                'docker-compose.dev.yml',
                'backend/config/settings.py',
                'README.md',
                '.env.example'
            ]
        }

    def get_user_input(self) -> Dict[str, str]:
        """Get user input for project configuration."""
        print("🚀 Welcome to App Template Setup!")
        print("=" * 50)
        print("This script will help you customize the template for your project.")
        print("Please provide the following information:\n")

        # Get display name
        display_name = input("📱 App Display Name (e.g., 'My Awesome App'): ").strip()
        if not display_name:
            print("❌ Display name cannot be empty!")
            sys.exit(1)

        # Get project name and suggest variants
        project_name = input("📦 Project Name (kebab-case, e.g., 'my-awesome-app'): ").strip()
        if not project_name:
            print("❌ Project name cannot be empty!")
            sys.exit(1)
        
        # Validate kebab-case
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', project_name):
            print("⚠️  Project name should be in kebab-case (lowercase, hyphens only)")
            confirm = input("Continue anyway? (y/N): ").strip().lower()
            if confirm != 'y':
                sys.exit(1)

        # Generate snake_case version
        suggested_snake = project_name.replace('-', '_')
        snake_name = input(f"🐍 Snake Case Name (for database/package, default: '{suggested_snake}'): ").strip()
        if not snake_name:
            snake_name = suggested_snake

        # Get database name
        database_name = input(f"🗄️  Database Name (default: '{snake_name}'): ").strip()
        if not database_name:
            database_name = snake_name

        # Get bucket name
        bucket_name = input(f"🪣 S3 Bucket Name (default: '{project_name}'): ").strip()
        if not bucket_name:
            bucket_name = project_name

        # Get Docker image prefix
        docker_prefix = input(f"🐳 Docker Image Prefix (default: '{project_name}'): ").strip()
        if not docker_prefix:
            docker_prefix = project_name

        # Get log file prefix
        log_prefix = input(f"📝 Log File Prefix (default: '{snake_name}'): ").strip()
        if not log_prefix:
            log_prefix = snake_name

        return {
            'display_name': display_name,
            'kebab_name': project_name,
            'snake_name': snake_name,
            'database_name': database_name,
            'bucket_name': bucket_name,
            'docker_prefix': docker_prefix,
            'log_prefix': log_prefix
        }

    def confirm_changes(self, config: Dict[str, str]) -> bool:
        """Show user what will be changed and ask for confirmation."""
        print("\n" + "=" * 50)
        print("📋 Configuration Summary")
        print("=" * 50)
        print(f"Display Name:     '{config['display_name']}'")
        print(f"Project Name:     '{config['kebab_name']}'")
        print(f"Package Name:     '{config['snake_name']}'")
        print(f"Database Name:    '{config['database_name']}'")
        print(f"Bucket Name:      '{config['bucket_name']}'")
        print(f"Docker Prefix:    '{config['docker_prefix']}'")
        print(f"Log Prefix:       '{config['log_prefix']}'")
        
        print("\n🔄 The following replacements will be made:")
        print(f"  'App Template' → '{config['display_name']}'")
        print(f"  'app-template' → '{config['kebab_name']}'")
        print(f"  'app_template' → '{config['snake_name']}'")
        print(f"  Database: 'app_template' → '{config['database_name']}'")
        print(f"  Bucket: 'app-template' → '{config['bucket_name']}'")
        print(f"  Docker images: 'app-template-*' → '{config['docker_prefix']}-*'")
        print(f"  Log files: 'app_template_*' → '{config['log_prefix']}_*'")
        
        print(f"\n📁 Files to be modified: {self._count_files_to_modify()}")
        
        confirm = input("\n✅ Proceed with these changes? (y/N): ").strip().lower()
        return confirm == 'y'

    def _count_files_to_modify(self) -> int:
        """Count total number of files that will be modified."""
        files = set()
        for file_list in self.file_replacements.values():
            files.update(file_list)
        return len(files)

    def backup_files(self) -> str:
        """Create a backup of the original files."""
        backup_dir = self.root_dir / 'backup_original'
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        backup_dir.mkdir()
        
        files_to_backup = set()
        for file_list in self.file_replacements.values():
            files_to_backup.update(file_list)
        
        for file_path in files_to_backup:
            src = self.root_dir / file_path
            if src.exists():
                dst = backup_dir / file_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        
        print(f"📁 Backup created at: {backup_dir}")
        return str(backup_dir)

    def apply_replacements(self, config: Dict[str, str]) -> None:
        """Apply all replacements to the files."""
        print("\n🔄 Applying replacements...")
        
        # Define specific replacement patterns
        replacements = [
            # Display name replacements
            ('App Template', config['display_name']),
            
            # Specific context replacements
            ('app-template-backend:latest', f"{config['docker_prefix']}-backend:latest"),
            ('app-template-web:latest', f"{config['docker_prefix']}-web:latest"),
            ('app-template', config['bucket_name']),  # This will handle bucket names
            
            # Database specific
            ('DB_NAME: ${DB_NAME:-app_template}', f"DB_NAME: ${{DB_NAME:-{config['database_name']}}}"),
            ('CREATE DATABASE app_template;', f"CREATE DATABASE {config['database_name']};"),
            
            # Log file specific
            ('app_template_backend_errors.log', f"{config['log_prefix']}_backend_errors.log"),
            
            # Package name in root package.json
            ('"name": "app_template"', f'"name": "{config["snake_name"]}"'),
            
            # General kebab-case (after specific ones to avoid conflicts)
            ('app-template', config['kebab_name']),
            
            # General snake_case (after specific ones to avoid conflicts)  
            ('app_template', config['snake_name']),
        ]
        
        modified_files = []
        
        for old_text, new_text in replacements:
            if old_text == new_text:
                continue
                
            for root, dirs, files in os.walk(self.root_dir):
                # Skip backup directory
                if 'backup_original' in root:
                    continue
                    
                for file in files:
                    if file.endswith(('.py', '.vue', '.js', '.ts', '.json', '.yml', '.yaml', '.sh', '.sql', '.md')):
                        file_path = Path(root) / file
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            if old_text in content:
                                new_content = content.replace(old_text, new_text)
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(new_content)
                                
                                if str(file_path.relative_to(self.root_dir)) not in modified_files:
                                    modified_files.append(str(file_path.relative_to(self.root_dir)))
                                    
                        except (UnicodeDecodeError, PermissionError):
                            # Skip binary files or files we can't read
                            continue
        
        print(f"✅ Modified {len(modified_files)} files:")
        for file_path in sorted(modified_files):
            print(f"   📝 {file_path}")

    def cleanup_setup_files(self) -> None:
        """Remove setup-related files that are no longer needed."""
        setup_files = ['setup.py', 'SETUP_GUIDE.md']
        
        print(f"\n🧹 Cleaning up setup files...")
        for file_name in setup_files:
            file_path = self.root_dir / file_name
            if file_path.exists():
                print(f"   🗑️  Removing {file_name}")
                file_path.unlink()

    def update_readme(self, config: Dict[str, str]) -> None:
        """Update README with project-specific information."""
        readme_path = self.root_dir / 'README.md'
        if not readme_path.exists():
            return
            
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the setup instructions section
        setup_section_pattern = r'Goal: Rename.*?grep -rl.*?\n'
        content = re.sub(setup_section_pattern, '', content, flags=re.DOTALL)
        
        # Update the title
        content = re.sub(r'^## .*? \(Monorepo\)', f'## {config["display_name"]} (Monorepo)', content, flags=re.MULTILINE)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("📝 Updated README.md")

    def run(self) -> None:
        """Run the complete setup process."""
        try:
            # Get user configuration
            config = self.get_user_input()
            
            # Confirm changes
            if not self.confirm_changes(config):
                print("❌ Setup cancelled by user.")
                sys.exit(0)
            
            # Create backup
            backup_dir = self.backup_files()
            
            # Apply replacements
            self.apply_replacements(config)
            
            # Update README
            self.update_readme(config)
            
            # Success message
            print("\n" + "=" * 50)
            print("🎉 Setup completed successfully!")
            print("=" * 50)
            print(f"✅ Your project '{config['display_name']}' is ready!")
            print(f"📁 Original files backed up to: {backup_dir}")
            print("\n🚀 Next steps:")
            print("1. Review the changes made to your files")
            print("2. Update environment variables in your .env files")
            print("3. Run your project with the new configuration")
            print("4. Delete the backup folder when you're satisfied with the changes")
            
            # Ask about cleanup
            cleanup = input("\n🧹 Remove setup script? (y/N): ").strip().lower()
            if cleanup == 'y':
                self.cleanup_setup_files()
                print("✅ Setup script removed")
            
            # Ask about backup folder cleanup
            cleanup_backup = input("🗂️  Remove backup folder? (y/N): ").strip().lower()
            if cleanup_backup == 'y':
                if Path(backup_dir).exists():
                    shutil.rmtree(backup_dir)
                    print("✅ Backup folder removed")
                else:
                    print("ℹ️  Backup folder already removed")

            
                
        except KeyboardInterrupt:
            print("\n❌ Setup cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error during setup: {e}")
            sys.exit(1)


if __name__ == "__main__":
    setup = ProjectSetup()
    setup.run()
