#!/usr/bin/env python3
"""
Script to fix the Python path issue for the Liquor Management System tests.
This script modifies the pytest.ini file to include the src directory in the Python path.
"""

import os
import sys

def fix_pytest_ini():
    """
    Fix the pytest.ini file to include the src directory in the Python path.
    """
    pytest_ini_path = 'pytest.ini'
    
    # Check if pytest.ini exists
    if not os.path.exists(pytest_ini_path):
        print(f"Creating {pytest_ini_path}...")
        with open(pytest_ini_path, 'w') as f:
            f.write("[pytest]\n")
    
    # Read the current content
    with open(pytest_ini_path, 'r') as f:
        content = f.read()
    
    # Check if python_paths is already defined
    if 'python_paths' in content:
        print(f"python_paths already defined in {pytest_ini_path}")
        return
    
    # Add python_paths
    with open(pytest_ini_path, 'a') as f:
        f.write("\n# Add src directory to Python path\n")
        f.write("python_paths = src\n")
    
    print(f"Added python_paths to {pytest_ini_path}")

def fix_run_tests_py():
    """
    Fix the run_tests.py script to add the src directory to the Python path.
    """
    run_tests_py_path = 'run_tests.py'
    
    # Check if run_tests.py exists
    if not os.path.exists(run_tests_py_path):
        print(f"{run_tests_py_path} not found")
        return
    
    # Read the current content
    with open(run_tests_py_path, 'r') as f:
        content = f.readlines()
    
    # Check if sys.path.append is already added
    for line in content:
        if 'sys.path.append' in line and 'src' in line:
            print(f"sys.path.append already added in {run_tests_py_path}")
            return
    
    # Find the import section
    import_section_end = 0
    for i, line in enumerate(content):
        if line.startswith('import') or line.startswith('from'):
            import_section_end = i + 1
    
    # Add sys.path.append after the import section
    content.insert(import_section_end, "\n# Add src directory to Python path\n")
    content.insert(import_section_end + 1, "sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))\n")
    
    # Write the modified content
    with open(run_tests_py_path, 'w') as f:
        f.writelines(content)
    
    print(f"Added sys.path.append to {run_tests_py_path}")

def create_pyproject_toml():
    """
    Create a pyproject.toml file to configure pytest.
    """
    pyproject_toml_path = 'pyproject.toml'
    
    # Check if pyproject.toml exists
    if os.path.exists(pyproject_toml_path):
        print(f"{pyproject_toml_path} already exists")
        return
    
    # Create pyproject.toml
    with open(pyproject_toml_path, 'w') as f:
        f.write("[tool.pytest.ini_options]\n")
        f.write("pythonpath = [\n")
        f.write("    \"src\",\n")
        f.write("]\n")
    
    print(f"Created {pyproject_toml_path}")

def create_conftest_py():
    """
    Create a conftest.py file in the root directory to add the src directory to the Python path.
    """
    conftest_py_path = 'conftest.py'
    
    # Check if conftest.py exists
    if os.path.exists(conftest_py_path):
        print(f"{conftest_py_path} already exists")
        return
    
    # Create conftest.py
    with open(conftest_py_path, 'w') as f:
        f.write("import os\n")
        f.write("import sys\n")
        f.write("\n")
        f.write("# Add src directory to Python path\n")
        f.write("sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))\n")
    
    print(f"Created {conftest_py_path}")

def main():
    """
    Main function.
    """
    print("Fixing Python path for Liquor Management System tests...")
    
    # Fix pytest.ini
    fix_pytest_ini()
    
    # Fix run_tests.py
    fix_run_tests_py()
    
    # Create pyproject.toml
    create_pyproject_toml()
    
    # Create conftest.py
    create_conftest_py()
    
    print("Done!")

if __name__ == '__main__':
    main()
