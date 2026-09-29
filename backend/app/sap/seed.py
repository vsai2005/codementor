"""Deploy-time SAP seeding: create missing Enterprise Missions and refresh their definitions.

Run after migrations and before the server starts (render.yaml and the Dockerfile do this):

    python -m app.sap.seed

Idempotent, and safe when several instances start at once. Request handlers only check
that the missions exist, so learners never pay the seeding cost.
"""

from __future__ import annotations

from app.database import SessionLocal
from app.sap.services.missions import SAPMissionService


def seed() -> int:
    with SessionLocal() as db:
        missions = SAPMissionService.seed_missions_if_needed(db)
    return len(missions)


if __name__ == "__main__":
    print(f"SAP missions seeded/refreshed: {seed()}")
