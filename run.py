#!/usr/bin/env python3
"""BitePlate - Smart Restaurant Management System - Quick Launch"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from main import BitePlateApp

if __name__ == "__main__":
    app = BitePlateApp()
    app.run()
