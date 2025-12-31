import sys
import os

# Add src to sys.path so we can import modules from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from main import main
    main()
