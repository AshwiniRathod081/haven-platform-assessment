from pathlib import Path

from scripts.cost_tag_check import (
    check_plan,
    find_missing_tag_addresses,
)


PLAN_FILE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "plan.json"
)


def test_fixture_flags_resources_missing_landlord_tag(capsys):
    """
    Verify that the actual Terraform plan identifies the expected
    resources missing landlord_account_id.
    """
    exit_code = check_plan(str(PLAN_FILE))
    output = capsys.readouterr().out

    assert exit_code == 1

    # These resources must fail.
    assert "listing_media" in output
    assert "mls_feed_sync" in output

    # These resources must pass.
    assert "landlord_media[0]" not in output
    assert "screening_report_export" not in output


def test_check_is_idempotent(capsys):
    """
    Running the check twice against the same plan must produce
    the same exit code and output.
    """
    first_exit_code = check_plan(str(PLAN_FILE))
    first_output = capsys.readouterr().out

    second_exit_code = check_plan(str(PLAN_FILE))
    second_output = capsys.readouterr().out

    assert first_exit_code == second_exit_code
    assert first_output == second_output

    # Each missing resource should appear only once per run.
    assert first_output.count("listing_media") == 1
    assert first_output.count("mls_feed_sync") == 1


def test_check_is_generic_and_skips_noop_and_delete_changes():
    """
    Verify the check works for different resource types and
    ignores resources that are not being created or updated.
    """
    plan = {
        "resource_changes": [
            {
                "type": "aws_s3_bucket",
                "address": "aws_s3_bucket.example",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "tags": {
                            "landlord_account_id": "la-001"
                        }
                    },
                },
            },
            {
                "type": "aws_lambda_function",
                "address": "aws_lambda_function.example",
                "change": {
                    "actions": ["update"],
                    "after": {
                        "tags": {
                            "tenant_id": "tenant-001"
                        }
                    },
                },
            },
            {
                "type": "aws_s3_bucket",
                "address": "aws_s3_bucket.noop",
                "change": {
                    "actions": ["no-op"],
                    "after": {
                        "tags": {}
                    },
                },
            },
            {
                "type": "aws_s3_bucket",
                "address": "aws_s3_bucket.deleted",
                "change": {
                    "actions": ["delete"],
                    "after": None,
                },
            },
        ]
    }

    missing = find_missing_tag_addresses(plan)

    assert missing == ["aws_lambda_function.example"]