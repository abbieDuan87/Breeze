import subprocess
from breeze.app import BreezeApp


def run_seeder():
    try:
        subprocess.run(["python", "data/seeder.py"], check=True)
        print("Seeder script ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running seeder.py: {e}")


def main():
    run_seeder()

    app = BreezeApp()
    app.run()


if __name__ == "__main__":
    main()
