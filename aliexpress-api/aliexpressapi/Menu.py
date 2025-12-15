import os
import sys
import subprocess
import shutil
import django
import time
from pathlib import Path
from threading import Thread
from django.db import connections

from django.conf import settings


# ======================================================
# Spinner
# ======================================================
class Spinner:
    def __init__(self, message="Processing..."):
        self.message = message
        self.running = False
        self.spinner_cycle = ["|", "/", "-", "\\"]

    def start(self):
        self.running = True
        Thread(target=self._spin, daemon=True).start()

    def _spin(self):
        idx = 0
        while self.running:
            print(
                f"\r{self.message} {self.spinner_cycle[idx % len(self.spinner_cycle)]}",
                end="",
            )
            idx += 1
            time.sleep(0.08)

    def stop(self):
        self.running = False
        print("\r", end="")


# ======================================================
# Timer
# ======================================================
class Timer:
    def __init__(self, label="Elapsed"):
        self.label = label
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is None:
            print("⚠️ Timer not started.")
            return None
        elapsed = time.time() - self.start_time
        print(f"⏱️ {self.label}: {elapsed:.2f} seconds")
        return elapsed


# ======================================================
# Helpers
# ======================================================
def run_cmd(cmd, show_spinner=False, message=None):
    if show_spinner and message:
        spinner = Spinner(message)
        spinner.start()
        result = subprocess.run(cmd, shell=True)
        spinner.stop()
    else:
        result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(result.returncode)


def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created folder: {path}")


# ======================================================
# Cleaners
# ======================================================
class Cleaner:
    def __init__(self, path: Path):
        self.path = path

    def exists(self) -> bool:
        return self.path.exists()


# class DatabaseCleaner(Cleaner):
#     def __init__(self, path: Path, retries: int = 6, delay: float = 0.6):
#         super().__init__(path)
#         self.retries = retries
#         self.delay = delay

#     def clean(self):
#         if not self.exists():
#             print("No DB file found")
#             return

#         try:
#             connections.close_all()
#         except:
#             pass

#         spinner = Spinner(f"Deleting DB: {self.path}")
#         spinner.start()

#         for _ in range(self.retries):
#             try:
#                 self.path.unlink()
#                 spinner.stop()
#                 print("🗑️ Database deleted")
#                 return
#             except:
#                 time.sleep(self.delay)

#         spinner.stop()
#         print("❌ Database could not be deleted. Close apps using DB.")
#         raise PermissionError("File locked!")


class CrossDatabaseCleaner:
    """
    Cross-database cleaner for Django projects.

    ✔ Supports SQLite & PostgreSQL
    ✔ Automatically detects active DB engine
    ✔ Refuses to run outside DEBUG mode (safety)

    ------------------------------------------------
    🔐 ENV REFERENCE (DO NOT COMMIT REAL SECRETS)
    ------------------------------------------------
    DEBUG=True
    ALLOWED_HOSTS=*
    SECRET_KEY=django-insecure-56%_hh9#xap(yrbv+_yjn_286)t(@blufv77)a%yof89#awv^6

    DB_NAME=portfolio
    DB_USER=postgres
    DB_PASS=admin
    DB_HOST=localhost
    DB_PORT=5432
    ------------------------------------------------
    """

    def clean(self):
        # ------------------------------------------------
        # SAFETY GUARD — NEVER RESET DB IN PROD
        # ------------------------------------------------
        if not settings.DEBUG:
            raise RuntimeError(
                "❌ Refusing to reset database because DEBUG=False. "
                "This operation is allowed only in development."
            )

        db = settings.DATABASES["default"]
        engine = db["ENGINE"]

        # Close all active Django DB connections
        try:
            connections.close_all()
        except Exception:
            pass

        # ------------------------------------------------
        # SQLITE CLEANUP
        # ------------------------------------------------
        if "sqlite3" in engine:
            db_path = Path(db["NAME"])

            if db_path.exists():
                db_path.unlink()
                print(f"🗑️ SQLite database deleted: {db_path}")
            else:
                print("ℹ️ SQLite database not found")

        # ------------------------------------------------
        # POSTGRESQL CLEANUP
        # ------------------------------------------------
        elif "postgresql" in engine:
            db_name = db["NAME"]
            db_user = db.get("USER", "postgres")

            print("🗑️ Resetting PostgreSQL database...")

            subprocess.run(
                f'psql -U {db_user} -c "DROP DATABASE IF EXISTS {db_name};"',
                shell=True,
                check=False,
            )
            subprocess.run(
                f'psql -U {db_user} -c "CREATE DATABASE {db_name};"',
                shell=True,
                check=False,
            )

            print("✅ PostgreSQL database recreated")

        # ------------------------------------------------
        # UNSUPPORTED DATABASE
        # ------------------------------------------------
        else:
            raise RuntimeError(f"❌ Unsupported DB engine: {engine}")


class PycacheCleaner(Cleaner):
    def clean(self):
        for p in self.path.rglob("__pycache__"):
            if p.is_dir():
                shutil.rmtree(p)
                print("🧹 Removed:", p)


class MigrationsCleaner(Cleaner):
    def clean(self):
        if not self.exists():
            print("❌ Apps path does not exist")
            return

        removed = False

        for migrations_dir in self.path.rglob("migrations"):
            if not migrations_dir.is_dir():
                continue

            for file in migrations_dir.iterdir():
                if (
                    file.is_file()
                    and file.name != "__init__.py"
                    and file.suffix == ".py"
                ):
                    file.unlink()
                    print("🧹 Removed:", file)
                    removed = True

        if not removed:
            print("✔️ No migration files to remove")


# ======================================================
# Migration + Superuser
# ======================================================
class MigrationAndSuperuser:
    def run(self):
        run_cmd(
            "python manage.py makemigrations",
            show_spinner=True,
            message="Making migrations",
        )
        run_cmd(
            "python manage.py migrate", show_spinner=True, message="Applying migrations"
        )

        print("Checking superuser...")
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username="admin", email="admin@gmail.com", password="admin"
            )
            print("👑 Superuser created")
        else:
            print("✔️ Superuser already exists")


# ======================================================
# Fixture Loader
# ======================================================
class FixtureLoader:
    def __init__(self, fixture_path, retries=3, delay=1.5):
        self.fixture_path = fixture_path
        self.retries = retries
        self.delay = delay

    def load(self):
        attempt = 1
        while attempt <= self.retries:
            result = subprocess.run(
                f"python manage.py loaddata {self.fixture_path}", shell=True
            )
            if result.returncode == 0:
                print("📦 Fixtures loaded successfully")
                return
            time.sleep(self.delay)
            attempt += 1
        print("❌ Failed loading fixtures")


# ======================================================
# NEW CLASS: GenerateFixtures
# ======================================================
class GenerateFixtures:
    """Reusable fixture generator class for future projects."""

    def run(self):
        print("🔄 Generating fixtures...")
        run_cmd("uv run manage.py generate_fixtures")
        run_cmd("uv run manage.py generate_homepage_fixtures")
        print("✨ Fixture generation completed!")


# ======================================================
# MENU
# ======================================================
def menu():
    print("\n=== Automation Menu ===")
    print("1️⃣ Remove DB")
    print("2️⃣ Remove __pycache__")
    print("3️⃣ Remove migration files")
    print("4️⃣ Run migrations + Ensure Superuser")
    print("5️⃣ Load Products Fixture")
    print("6️⃣ FULL RESET (DB + Pycache + Migrations + Migrate)")
    print("7️⃣ Generate Fixtures (NEW)")
    print("0️⃣ Exit")
    return input("Choose: ").strip()


# ======================================================
# MAIN LOOP
# ======================================================
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")
    django.setup()

    # apps_path = Path("./apps")
    db_file = Path("./database/db.sqlite3")

    apps_path = Path("./apps")
    db_folder = Path("./database")

    # Ensure required folders exist
    # ensure_dir(apps_path)
    ensure_dir(db_folder)
    # ensure_dir(fixtures_folder)

    while True:
        choice = menu()

        if choice == "1":
            # DatabaseCleaner(db_file).clean()
            CrossDatabaseCleaner().clean()

        elif choice == "2":
            PycacheCleaner(apps_path).clean()

        elif choice == "3":
            MigrationsCleaner(apps_path).clean()

        elif choice == "4":
            MigrationAndSuperuser().run()

        elif choice == "5":
            FixtureLoader("fixtures/products_fixture.json").load()

        elif choice == "6":
            print("⚠️ FULL RESET...")
            # DatabaseCleaner(db_file).clean()
            CrossDatabaseCleaner().clean()
            PycacheCleaner(apps_path).clean()
            MigrationsCleaner(apps_path).clean()
            # MigrationAndSuperuser().run()
            print("🚀 FULL RESET DONE!")

        elif choice == "7":
            MigrationAndSuperuser().run()
            GenerateFixtures().run()

        elif choice == "0":
            print("Bye 👋")
            break

        else:
            print("Invalid option!")
