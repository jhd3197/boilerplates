import os
import shutil
import re

def get_valid_input(prompt, default=None):
    while True:
        user_input = input(prompt)
        if not user_input and default:
            return default
        if user_input:
            return user_input

def sanitize_package_name(name):
    """Sanitizes a project name to be a valid Python package name."""
    # Remove invalid characters, replace - with _, ensure mostly alphanumeric
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    name = re.sub(r'^[^a-zA-Z_]+', '', name) # Must start with letter or underscore
    return name.lower()

def replace_in_file(filepath, old_str, new_str):
    """Reads a file, replaces occurences of old_str with new_str, and writes it back."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace(old_str, new_str)
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"Warning: Could not process {filepath}: {e}")
    return False

def main():
    print("Welcome to the Boilerplate Initializer!")
    
    # Define templates path (relative to this script)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_root = os.path.join(base_dir, 'python')
    
    if not os.path.exists(templates_root):
        print(f"Error: Templates directory not found at {templates_root}")
        return

    # 1. List Templates
    templates = [d for d in os.listdir(templates_root) if os.path.isdir(os.path.join(templates_root, d))]
    
    if not templates:
        print("No templates found.")
        return

    print("\nAvailable Templates:")
    for idx, t in enumerate(templates):
        print(f"{idx + 1}. {t}")

    # 2. Select Template
    while True:
        try:
            choice = input("\nSelect a template number: ")
            template_idx = int(choice) - 1
            if 0 <= template_idx < len(templates):
                template_name = templates[template_idx]
                break
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

    selected_template_path = os.path.join(templates_root, template_name)

    # 3. Project Name
    project_name = get_valid_input("\nEnter new project name (folder name): ")
    
    # 4. Package Name (for replacement)
    default_pkg_name = sanitize_package_name(project_name)
    package_name = get_valid_input(f"Enter python package name (default: {default_pkg_name}): ", default_pkg_name)
    package_name = sanitize_package_name(package_name)

    target_dir = os.path.join(os.getcwd(), project_name)

    if os.path.exists(target_dir):
        print(f"Error: Directory '{project_name}' already exists.")
        return

    print(f"\nInitializing project '{project_name}' from '{template_name}'...")
    print(f"Package name will be: {package_name}")

    # Copy template
    try:
        shutil.copytree(selected_template_path, target_dir)
    except Exception as e:
        print(f"Error copying template: {e}")
        return

    # Rename 'myproject' directory if it exists
    old_pkg_name = 'myproject'
    old_pkg_path = os.path.join(target_dir, old_pkg_name)
    new_pkg_path = os.path.join(target_dir, package_name)

    if os.path.exists(old_pkg_path):
        os.rename(old_pkg_path, new_pkg_path)
        print(f"Renamed package directory '{old_pkg_name}' to '{package_name}'")
    else:
        print(f"Warning: Expected package directory '{old_pkg_name}' not found in template.")

    # Find and replace in files
    print("Updating file contents...")
    count = 0
    for root, dirs, files in os.walk(target_dir):
        # sensitive ignore directories to save time/errors (like __pycache__, .git)
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        
        for file in files:
            # Skip binary or irrelevant files
            if file.endswith(('.pyc', '.png', '.jpg', '.git')):
                continue
                
            file_path = os.path.join(root, file)
            if replace_in_file(file_path, old_pkg_name, package_name):
                count += 1
    
    print(f"Updated {count} files.")
    print(f"\nSuccess! Project '{project_name}' created.")
    print(f"Next steps:")
    print(f"  cd {project_name}")
    print("  # Follow the README.md instructions inside the project")

if __name__ == "__main__":
    main()
