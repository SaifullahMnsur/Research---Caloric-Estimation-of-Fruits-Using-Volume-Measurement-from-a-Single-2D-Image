import subprocess
import sys

def install_packages(scope):
    packages = [
        "ultralytics",
        "datetime",
        "numpy",
        "scipy",
        "matplotlib"
    ]
    
    flag = "--user" if scope == "user" else ""

    for package in packages:
        if flag:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, flag])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("Where would you like to install the packages?")
    print("1. Current user")
    print("2. Whole system")
    choice = input("Enter the number of your choice (1 or 2): ").strip()
    
    if choice == "1":
        install_packages("user")
    elif choice == "2":
        install_packages("all")
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
