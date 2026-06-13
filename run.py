#!/usr/bin/env python
"""BitePlate Web - Run server"""
import os
import sys

# Add src/ to path BEFORE any imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biteplate_web.settings')

    from django.core.management import execute_from_command_line

    print("=" * 50)
    print("  BITEPLATE - Smart Restaurant Management System")
    print("  Web Version (Django)")
    print("=" * 50)
    print()
    print("Starting development server...")
    print("http://127.0.0.1:8000/")
    print()
    print("Default Login Credentials:")
    print("  manager / admin123")
    print("  chef / chef123")
    print("  waiter / waiter123")
    print("  cashier / cashier123")
    print()

    execute_from_command_line([sys.argv[0], 'runserver', '--noreload'])

if __name__ == '__main__':
    main()
