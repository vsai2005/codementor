"""SAP Enterprise Digital Twin Service.

Manages persistent fictional enterprise definitions and per-learner instances.
Provides deterministic state mutations and auditable training scenario resets.
"""

from __future__ import annotations

import copy
import uuid
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sap_models import SAPEnterprise, SAPEnterpriseInstance


NOVA_MANUFACTURING_TEMPLATE: dict[str, Any] = {
    "slug": "nova-manufacturing",
    "name": "Nova Manufacturing Corp",
    "code": "NM01",
    "industry": "High-Tech Industrial Automation",
    "description_md": """
Nova Manufacturing Corp (NM01) is a mid-sized enterprise producing next-generation
industrial automation controllers, IoT sensor hubs, and high-precision assembly robotics.
Headquartered in Heidelberg with regional manufacturing and R&D facilities across Europe and North America.
""".strip(),
    "template_state": {
        "company_code": {
            "code": "NM01",
            "name": "Nova Manufacturing AG",
            "currency": "EUR",
            "country": "DE",
            "chart_of_accounts": "YCOA",
            "fiscal_year_variant": "K4",
        },
        "plants": [
            {
                "id": "PL01",
                "name": "Heidelberg Main Assembly",
                "country": "DE",
                "company_code": "NM01",
                "storage_locations": ["RM01", "FG01", "SP01"],
            },
            {
                "id": "PL02",
                "name": "Austin Tech Center",
                "country": "US",
                "company_code": "NM01",
                "storage_locations": ["RM01", "FG01"],
            },
        ],
        "storage_locations": [
            {"id": "RM01", "name": "Raw Materials Warehouse", "plant_id": "PL01"},
            {"id": "FG01", "name": "Finished Goods Central", "plant_id": "PL01"},
            {"id": "SP01", "name": "Spare Parts & Service Depot", "plant_id": "PL01"},
            {"id": "RM01", "name": "Austin Inbound Staging", "plant_id": "PL02"},
            {"id": "FG01", "name": "Austin Distribution Bay", "plant_id": "PL02"},
        ],
        "purchasing_organizations": [
            {
                "id": "PO01",
                "name": "Global Procurement Org",
                "company_code": "NM01",
                "assigned_plants": ["PL01", "PL02"],
            },
        ],
        "sales_organizations": [
            {
                "id": "SO01",
                "name": "Direct Enterprise Sales",
                "company_code": "NM01",
                "distribution_channels": ["DC01", "DC02"],
                "divisions": ["DV01"],
            },
        ],
        "suppliers": [
            {
                "id": "VEND-101",
                "name": "Rheinland Precision Metal GmbH",
                "city": "Stuttgart",
                "country": "DE",
                "reconciliation_account": "16000000",
                "payment_terms": "NT30",
            },
            {
                "id": "VEND-102",
                "name": "Silicon Bavaria Sensors AG",
                "city": "Munich",
                "country": "DE",
                "reconciliation_account": "16000000",
                "payment_terms": "14D2",
            },
        ],
        "customers": [
            {
                "id": "CUST-501",
                "name": "Nordics Heavy Industrial AB",
                "city": "Stockholm",
                "country": "SE",
                "reconciliation_account": "12100000",
                "sales_org": "SO01",
            },
            {
                "id": "CUST-502",
                "name": "Alpine Automation AG",
                "city": "Zurich",
                "country": "CH",
                "reconciliation_account": "12100000",
                "sales_org": "SO01",
            },
        ],
        "materials": [
            {
                "sku": "DXTR-1000",
                "description": "Industrial Sensor Controller Hub",
                "type": "FERT",
                "base_uom": "EA",
                "valuation_price": 450.00,
                "currency": "EUR",
                "plant_id": "PL01",
            },
            {
                "sku": "CHAS-2000",
                "description": "Milled Aluminum Controller Chassis",
                "type": "ROH",
                "base_uom": "EA",
                "valuation_price": 85.00,
                "currency": "EUR",
                "plant_id": "PL01",
            },
            {
                "sku": "SENS-3000",
                "description": "Optical Telemetry Sensor Module",
                "type": "ROH",
                "base_uom": "EA",
                "valuation_price": 120.00,
                "currency": "EUR",
                "plant_id": "PL01",
            },
        ],
        "boms": [
            {
                "parent_sku": "DXTR-1000",
                "plant_id": "PL01",
                "components": [
                    {"sku": "CHAS-2000", "quantity": 1, "uom": "EA"},
                    {"sku": "SENS-3000", "quantity": 2, "uom": "EA"},
                ],
            }
        ],
        "inventory": [
            {"plant_id": "PL01", "storage_loc": "RM01", "sku": "CHAS-2000", "stock": 1200},
            {"plant_id": "PL01", "storage_loc": "RM01", "sku": "SENS-3000", "stock": 2400},
            {"plant_id": "PL01", "storage_loc": "FG01", "sku": "DXTR-1000", "stock": 350},
        ],
        "finance_state": {
            "cash_bank_eur": 1500000.00,
            "accounts_payable_eur": 340000.00,
            "accounts_receivable_eur": 680000.00,
            "inventory_valuation_eur": 463500.00,
        },
    },
    "landscape_metadata": {
        "s4hana_version": "2023 FPS02 (Private Cloud / On-Premise Core)",
        "client": "100",
        "system_id": "PRD",
        "clean_core_compliance": "Tier-1 Released APIs Enabled",
        "btp_subaccount": "nova-mfg-prod-eu10",
        "integration_suite_active": True,
    },
}


class SAPEnterpriseService:
    """Service layer managing the persistent enterprise digital twin and learner-specific state."""

    @classmethod
    def get_or_create_template(cls, db: Session, slug: str = "nova-manufacturing") -> SAPEnterprise:
        """Ensures the enterprise template exists in the database."""
        enterprise = db.execute(
            select(SAPEnterprise).where(SAPEnterprise.slug == slug)
        ).scalar_one_or_none()

        if enterprise is None:
            data = NOVA_MANUFACTURING_TEMPLATE
            enterprise = SAPEnterprise(
                slug=data["slug"],
                name=data["name"],
                code=data["code"],
                industry=data["industry"],
                description_md=data["description_md"],
                template_state=copy.deepcopy(data["template_state"]),
                landscape_metadata=copy.deepcopy(data["landscape_metadata"]),
                is_active=True,
            )
            db.add(enterprise)
            db.commit()
            db.refresh(enterprise)

        return enterprise

    @classmethod
    def get_or_create_instance(
        cls,
        db: Session,
        user_id: uuid.UUID,
        enterprise_slug: str = "nova-manufacturing",
    ) -> SAPEnterpriseInstance:
        """Retrieves or initializes an isolated persistent digital twin instance for a learner."""
        template = cls.get_or_create_template(db, slug=enterprise_slug)

        instance = db.execute(
            select(SAPEnterpriseInstance).where(
                SAPEnterpriseInstance.user_id == user_id,
                SAPEnterpriseInstance.enterprise_id == template.id,
            )
        ).scalar_one_or_none()

        if instance is None:
            now = datetime.now(timezone.utc)
            instance = SAPEnterpriseInstance(
                user_id=user_id,
                enterprise_id=template.id,
                state_version=1,
                status="active",
                company_state=copy.deepcopy(template.template_state),
                audit_log=[
                    {
                        "action": "INSTANCE_INITIALIZED",
                        "timestamp": now.isoformat(),
                        "details": f"Enterprise instance spawned from template '{template.name}'",
                    }
                ],
            )
            db.add(instance)
            db.commit()
            db.refresh(instance)

        return instance

    @classmethod
    def reset_instance(
        cls,
        db: Session,
        user_id: uuid.UUID,
        enterprise_slug: str = "nova-manufacturing",
    ) -> SAPEnterpriseInstance:
        """Safely resets the learner's digital twin company state back to the original template."""
        template = cls.get_or_create_template(db, slug=enterprise_slug)
        instance = cls.get_or_create_instance(db, user_id=user_id, enterprise_slug=enterprise_slug)

        now = datetime.now(timezone.utc)
        instance.company_state = copy.deepcopy(template.template_state)
        instance.state_version += 1
        instance.status = "reset"

        audit = list(instance.audit_log or [])
        audit.append({
            "action": "INSTANCE_RESET_TO_TEMPLATE",
            "timestamp": now.isoformat(),
            "state_version": instance.state_version,
        })
        instance.audit_log = audit[-50:]  # preserve last 50 audit entries

        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def apply_state_mutation(
        cls,
        db: Session,
        user_id: uuid.UUID,
        enterprise_slug: str,
        mutation_action: str,
        patch: dict[str, Any],
        mission_slug: str | None = None,
    ) -> SAPEnterpriseInstance:
        """Applies a deterministic, auditable state mutation to the learner's digital twin."""
        instance = cls.get_or_create_instance(db, user_id=user_id, enterprise_slug=enterprise_slug)

        state = copy.deepcopy(instance.company_state)
        # Deeply or shallowly apply patches deterministically
        for key, val in patch.items():
            if isinstance(val, list) and key in state and isinstance(state[key], list):
                # Append or update list items by id/code
                existing_keys = {item.get("id") or item.get("code") or item.get("sku"): idx
                                 for idx, item in enumerate(state[key]) if isinstance(item, dict)}
                for new_item in val:
                    if isinstance(new_item, dict):
                        item_id = new_item.get("id") or new_item.get("code") or new_item.get("sku")
                        if item_id and item_id in existing_keys:
                            state[key][existing_keys[item_id]].update(new_item)
                        else:
                            state[key].append(new_item)
                    else:
                        state[key].append(new_item)
            elif isinstance(val, dict) and key in state and isinstance(state[key], dict):
                state[key].update(val)
            else:
                state[key] = val

        now = datetime.now(timezone.utc)
        instance.company_state = state
        instance.state_version += 1

        audit = list(instance.audit_log or [])
        audit.append({
            "action": mutation_action,
            "mission_slug": mission_slug,
            "timestamp": now.isoformat(),
            "state_version": instance.state_version,
            "patch_keys": list(patch.keys()),
        })
        instance.audit_log = audit[-50:]

        db.commit()
        db.refresh(instance)
        return instance
