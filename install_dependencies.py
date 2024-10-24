import os
import platform
import subprocess
import sys


def install_linux_dependencies():
    try:
        # Update package lists and install required packages
        subprocess.check_call(["sudo", "apt-get", "update"])
        subprocess.check_call(
            [
                "sudo",
                "apt-get",
                "install",
                "-y",
                "python3-pyqt5",
                "sqlite3",
                "sqlitebrowser",
            ]
        )
        print("Linux dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation on Linux: {e}")


def install_mac_dependencies():
    try:
        # Check if Homebrew is installed
        if subprocess.call(["which", "brew"]) != 0:
            print("Homebrew not found. Installing Homebrew...")
            subprocess.check_call(
                [
                    "/bin/bash",
                    "-c",
                    "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)",
                ]
            )

        # Install dependencies using Homebrew
        subprocess.check_call(["brew", "install", "python"])
        subprocess.check_call(["brew", "install", "--cask", "db-browser-for-sqlite"])
        print("macOS dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation on macOS: {e}")


def install_windows_dependencies():
    try:
        # Install Python dependencies via pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyqt5"])

        print("Windows dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation on Windows: {e}")


def main():
    os_type = platform.system()

    if os_type == "Linux":
        install_linux_dependencies()
    elif os_type == "Darwin":  # macOS
        install_mac_dependencies()
    elif os_type == "Windows":
        install_windows_dependencies()
    else:
        print("Unsupported OS. Please install dependencies manually.")


if __name__ == "__main__":
    main()
