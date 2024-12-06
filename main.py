import os
import subprocess
import sys
from breeze.app import BreezeApp


def run_seeder():
    users_file_path = os.path.join("data", "users.json")
    seeder_script_path = os.path.join("data", "seeder.py")

    if not os.path.exists(users_file_path):
        try:
            subprocess.run([sys.executable, seeder_script_path], check=True)
            print("Seeder script ran successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running seeder.py: {e}")
    else:
        print("users.json already exists.")


def main():
    run_seeder()

    app = BreezeApp()
    app.run()


if __name__ == "__main__":
    main()
