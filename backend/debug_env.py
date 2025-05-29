import sys
import os

print("=== ENVIRONMENT DEBUG ===")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV', 'Not set')}")

print("\n=== PYTHON PATH ===")
for path in sys.path:
    print(f"  {path}")

print("\n=== PACKAGE TESTS ===")
packages_to_test = ['fastapi', 'uvicorn', 'pydantic', 'openai']

for package in packages_to_test:
    try:
        __import__(package)
        print(f"✅ {package} - OK")
    except ImportError as e:
        print(f"❌ {package} - FAILED: {e}")

print("\n=== INSTALLED PACKAGES ===")
try:
    import pkg_resources
    installed = [d.project_name for d in pkg_resources.working_set]
    for package in packages_to_test:
        if package in installed:
            print(f"✅ {package} installed")
        else:
            print(f"❌ {package} NOT installed")
except:
    print("Could not check installed packages")