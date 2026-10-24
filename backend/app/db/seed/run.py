# backend/app/db/seed/run.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from sqlalchemy.exc import IntegrityError
from app.db.session import SessionLocal

# Базовые сиды
from app.db.seed.initial_permissions import seed_permissions
from app.db.seed.initial_roles import seed_roles
from app.db.seed.initial_categories import seed_categories
from app.db.seed.initial_priorities import seed_priorities
from app.db.seed.initial_territories import seed_territories
from app.db.seed.initial_organizations import seed_organizations
from app.db.seed.initial_users import seed_users
from app.db.seed.initial_sla import seed_sla

# Демо-сиды
from app.db.seed.initial_geo_tags import seed_geo_tags
from app.db.seed.initial_problems import seed_problems
from app.db.seed.initial_initiatives import seed_initiatives
from app.db.seed.initial_events import seed_events
from app.db.seed.initial_messages import seed_messages
from app.db.seed.initial_notifications import seed_notifications


def run_all_seeds():
    db = SessionLocal()
    try:
        print("=" * 50)
        print(" STARTING DATABASE SEEDING ")
        print("=" * 50)

        # 1. Справочники и права
        print("\n--- Phase 1: Core Data ---")
        seed_permissions(db)
        seed_roles(db)
        seed_categories(db)
        seed_priorities(db)

        # 2. Инфраструктура и география
        print("\n--- Phase 2: Infrastructure ---")
        seed_territories(db)
        seed_organizations(db)

        # 3. Пользователи и настройки
        print("\n--- Phase 3: Users & Settings ---")
        seed_users(db)
        seed_sla(db)

        # 4. Демо-данные
        print("\n--- Phase 4: Demo Data ---")
        seed_geo_tags(db)
        seed_problems(db)
        seed_initiatives(db)
        seed_events(db)
        seed_messages(db)
        seed_notifications(db)

        print("\n" + "=" * 50)
        print(" ALL SEEDS COMPLETED SUCCESSFULLY! ")
        print("=" * 50)

    except IntegrityError as e:
        print(f"\n❌ Integrity Error during seeding: {e}")
        db.rollback()
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_all_seeds()