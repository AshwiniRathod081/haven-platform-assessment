"""
B2, part 1 — implement can_access_screening_report().

Read README.md's domain model first. A ScreeningReport belongs to a Tenant, a Tenant belongs to
a Property, and a Property belongs to a LandlordAccount. A PropertyManager is scoped to exactly
one LandlordAccount.

Work out from that hierarchy which boundary actually gates access to a ScreeningReport.
"""

from app.models import PropertyManager, ScreeningReport, Property, Tenant


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    Allow access only when the report's tenant belongs to a property
    owned by the PropertyManager's landlord account.

    Fail closed if any required relationship is missing.
    """

    # Step 1: Get the tenant associated with the screening report.
    tenant = next(
        (t for t in tenants if t.id == report.tenant_id),
        None
    )

    if tenant is None:
        return False

    # Step 2: Find the property associated with the tenant.
    property_record = next(
        (p for p in properties if p.id == tenant.property_id),
        None
    )

    if property_record is None:
        return False

    # Step 3: Get the landlord account IDs.
    manager_landlord_id = actor.landlord_account_id
    property_landlord_id = property_record.landlord_account_id

    # Step 4: Fail closed if ownership information is missing.
    if not manager_landlord_id or not property_landlord_id:
        return False

    # Step 5: Allow access only within the same landlord account.
    return manager_landlord_id == property_landlord_id
