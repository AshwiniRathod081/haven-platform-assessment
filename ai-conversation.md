AI-Assisted Development Log — B2
Evidence note: This file records the B2 development process and the actual issue/correction observed during this conversation. The explanatory sections below are summaries, not verbatim transcripts. Where the assignment asks for actual prompts and AI output, paste the corresponding messages directly from the ChatGPT conversation. Do not label summaries as verbatim dialogue.

1. Access control
Requirement
Implement can_access_screening_report(actor, report, *, properties, tenants) so that a Property Manager can view a screening report only when the report's tenant belongs to a property under the same landlord_account_id as the manager.

The relationship used is:

ScreeningReport → Tenant → Property → LandlordAccount

The check must fail closed if the tenant or property cannot be found.
Implementation approach
The implementation:
1. Finds the tenant referenced by report.tenant_id.
2. Returns False if that tenant does not exist.
3. Finds the property referenced by tenant.property_id.
4. Returns False if that property does not exist.
5. Returns False if either landlord account ID is missing.
6. Allows access only when actor.landlord_account_id equals the property's landlord_account_id.
Tests and observed result
The access-control tests cover:
- A manager from one landlord account attempting to access another account's report — denied.
- A manager accessing a report belonging to their own landlord account — allowed.
Observed result: both access-control tests passed.
Actual conversation evidence to paste
Paste the actual prompt(s) you sent about implementing can_access_screening_report() and the relevant AI response(s) from the conversation here.
2. Cost-tag validation
Requirement
Implement scripts/cost_tag_check.py to read a Terraform plan JSON file and validate that every resource being created or updated has the required landlord_account_id tag.

tenant_id is not the billing-unit tag and must not satisfy this requirement.
Implementation approach
The script:
- Reads and parses the Terraform plan JSON.
- Inspects resource_changes.
- Checks resources whose actions include create or update.
- Requires a non-empty landlord_account_id tag.
- Skips changes that are only delete, no-op, or read operations.
- Returns a non-zero exit code when required tags are missing.
- Prints missing resources in sorted order for deterministic output.
- Uses a set to avoid duplicate findings during one validation run.
Actual conversation evidence to paste
Paste the actual prompt(s) you sent about implementing the cost-tag validator and the relevant AI response(s) here.
3. AI mistake caught and corrected
This section records a real import-path mistake that occurred during test setup.
Initial incorrect import suggestion
from app.cost_tag_check import check_plan
Error encountered
ModuleNotFoundError: No module named 'app.cost_tag_check'
What was checked
The implementation file was located at:
scripts/cost_tag_check.py
The test was importing from the wrong package path.
Corrected import
from scripts.cost_tag_check import check_plan
Verification
After correcting the import, the four cost-tag tests passed.
Transcript requirement: Paste the actual ChatGPT message that suggested the incorrect import, your actual error message, and the actual correction message from the conversation here. Keep the exchange in its original wording. This summary is not a substitute for the actual transcript.

4. Idempotency and deterministic output
The exact finding key used by the validator is:

resource address + ":" + required tag name

Example:
aws_s3_bucket.listing_media:landlord_account_id
A Python set stores finding keys so the same resource/tag finding is not printed more than once within a validation run. Findings are sorted before printing, making the output deterministic.

Running the validator repeatedly against the same unchanged plan produces the same exit code and output. The script does not modify the plan or persist previously checked plans; repeatability comes from deterministic validation without external state.
Actual conversation evidence to paste
Paste the actual prompt(s) and AI response(s) discussing idempotency, the finding key, duplicate handling, and repeat-run verification here.
5. Test results
The final full test suite was run with:
python -m pytest -v
Observed result:
tests/test_access_control.py::test_denies_cross_account_access PASSED
tests/test_access_control.py::test_allows_same_account_access PASSED
tests/test_cost_tag_check.py::test_plan_with_missing_tags_fails PASSED
tests/test_cost_tag_check.py::test_plan_with_required_tags_passes PASSED
tests/test_cost_tag_check.py::test_noop_and_read_changes_are_skipped PASSED
tests/test_cost_tag_check.py::test_same_plan_produces_same_result_without_duplicate_output PASSED

6 passed
The cost-tag validator was also run twice against fixtures/plan.json. Both runs reported the missing landlord_account_id tag for:
- aws_lambda_function.mls_feed_sync
- aws_s3_bucket.listing_media
Both runs returned exit code 1, as expected for a plan containing resources without the required tag.
Actual conversation evidence to paste
If the assignment requires the actual AI output for the test/debugging discussion, paste the relevant original messages here rather than relying only on this summary.