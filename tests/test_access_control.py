"""
Write tests here proving:
  1. A PropertyManager scoped to la-001 (pm-001) is DENIED access to la-002's tenant's
     screening report (rep-002).
  2. The same PropertyManager (pm-001) IS allowed access to their own account's screening
     report (rep-001).

Use the `property_managers`, `properties`, `tenants`, and `screening_reports` fixtures from
conftest.py — don't re-invent the seed data here.
"""

from types import SimpleNamespace

import pytest

from app.access_control import can_access_screening_report


@pytest.fixture
def property_manager():
    return SimpleNamespace(
        id="pm-001",
        landlord_account_id="la-001"
    )


@pytest.fixture
def properties():
    return [
        SimpleNamespace(
            id="property-001",
            landlord_account_id="la-001"
        ),
        SimpleNamespace(
            id="property-002",
            landlord_account_id="la-002"
        )
    ]


@pytest.fixture
def tenants():
    return [
        SimpleNamespace(
            id="tenant-001",
            property_id="property-001"
        ),
        SimpleNamespace(
            id="tenant-002",
            property_id="property-002"
        )
    ]


def test_same_landlord_account_access_allowed(
    property_manager, properties, tenants
):
    """Property Manager should access reports under their own landlord."""

    report = SimpleNamespace(tenant_id="tenant-001")

    result = can_access_screening_report(
        property_manager,
        report,
        properties=properties,
        tenants=tenants
    )

    assert result is True


def test_cross_landlord_account_access_denied(
    property_manager, properties, tenants
):
    """Property Manager must not access another landlord's reports."""

    report = SimpleNamespace(tenant_id="tenant-002")

    result = can_access_screening_report(
        property_manager,
        report,
        properties=properties,
        tenants=tenants
    )

    assert result is False


def test_access_denied_when_tenant_not_found(
    property_manager, properties
):
    """Access should be denied if tenant does not exist."""

    report = SimpleNamespace(tenant_id="tenant-999")

    result = can_access_screening_report(
        property_manager,
        report,
        properties=properties,
        tenants=[]
    )

    assert result is False


def test_access_denied_when_property_not_found(
    property_manager, properties
):
    """Access should be denied if tenant's property does not exist."""

    report = SimpleNamespace(tenant_id="tenant-003")

    tenants = [
        SimpleNamespace(
            id="tenant-003",
            property_id="property-999"
        )
    ]

    result = can_access_screening_report(
        property_manager,
        report,
        properties=properties,
        tenants=tenants
    )

    assert result is False


def test_access_denied_when_landlord_account_missing(
    properties, tenants
):
    """Access should be denied when manager ownership is missing."""

    actor = SimpleNamespace(
        id="pm-002",
        landlord_account_id=None
    )

    report = SimpleNamespace(tenant_id="tenant-001")

    result = can_access_screening_report(
        actor,
        report,
        properties=properties,
        tenants=tenants
    )

    assert result is False

