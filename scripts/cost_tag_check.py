import json
import sys


REQUIRED_TAG = "landlord_account_id"


def find_missing_tag_addresses(plan: dict) -> list[str]:
    """
    Return addresses of created or updated resources that are missing
    the required landlord_account_id tag.
    """
    missing = set()

    for resource in plan.get("resource_changes", []):
        change = resource.get("change", {})
        actions = change.get("actions", [])

        # Check only resources being created or updated.
        # This also includes replacements, which contain "create".
        if not any(action in actions for action in ("create", "update")):
            continue

        address = resource.get("address", "<unknown-address>")
        after = change.get("after")

        tags = after.get("tags") if isinstance(after, dict) else None

        tag_value = tags.get(REQUIRED_TAG) if isinstance(tags, dict) else None

        # Missing, null, empty, or whitespace-only values are invalid.
        if not isinstance(tag_value, str) or not tag_value.strip():
            missing.add(address)

    # Sorting makes the output deterministic; set prevents duplicates.
    return sorted(missing)


def check_plan(plan_path: str) -> int:
    """
    Returns:
        0 if every created/updated resource has landlord_account_id.
        1 if one or more resources are missing the required tag.
        2 if the plan file cannot be read or parsed.
    """
    try:
        with open(plan_path, "r", encoding="utf-8") as file:
            plan = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Error reading Terraform plan: {error}", file=sys.stderr)
        return 2

    missing_resources = find_missing_tag_addresses(plan)

    if missing_resources:
        for address in missing_resources:
            print(f"Missing required tag '{REQUIRED_TAG}': {address}")

        return 1

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/cost_tag_check.py <plan.json>")
        sys.exit(2)

    sys.exit(check_plan(sys.argv[1]))