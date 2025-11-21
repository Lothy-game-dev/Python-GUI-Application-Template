import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask_migrate import Migrate, upgrade, migrate, init
from dotenv import load_dotenv
from app.database.sqlite import config_db, import_models

# Load environment variables from .env file
load_dotenv()


def init_db():
    db, app = config_db()
    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
    _ = Migrate(app, db)

    with app.app_context():
        import_models()
        print("Table imported:")
        for table in db.metadata.tables:
            print(table)

        db.create_all()
        if not os.path.isfile(os.path.join(migrations_dir, "env.py")):
            init(directory=os.environ.get("MIGRATION_DIR"))

        # Initialize the migration
        migrate(message="Initial migration", directory=os.environ.get("MIGRATION_DIR"))

        # Apply the migration
        upgrade(directory=os.environ.get("MIGRATION_DIR"))


def update_db():
    db, app = config_db()
    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
    _ = Migrate(app, db)

    with app.app_context():
        # Import models to ensure they are registered
        import_models()

        # Initialize the migration if not already done
        if not os.path.isfile(os.path.join(migrations_dir, "env.py")):
            init(directory=os.environ.get("MIGRATION_DIR"))

        # Create a new migration script
        migrate(directory=os.environ.get("MIGRATION_DIR"))

        # Apply the migration
        upgrade(directory=os.environ.get("MIGRATION_DIR"))

        print("Database updated with new migrations.")


def auto_process_db():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    if os.path.exists(os.path.join("./app/instance", "data.db")):
        update_db()
        print("Database updated successfully.")
    else:
        init_db()
        print("Database initialized successfully.")


if __name__ == "__main__":
    auto_process_db()
