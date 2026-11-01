# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide a plan has already been
checked/reported on. Use the word "idempotency" in your explanation.

## B2 — Cost tagging

The required cost-allocation tag is `landlord_account_id`, because the
landlord account is the actual billing unit. A `tenant_id` tag is not
sufficient because multiple tenants can belong to the same landlord account.

The cost-tagging check examines all resources being created or updated
in the Terraform plan. It fails when the `landlord_account_id` tag is
missing, null, or empty.

The check supports idempotency because it only reads the Terraform plan
and does not modify the plan or its resources. It produces deterministic
results by sorting and deduplicating missing resource addresses.
Running it repeatedly against the same plan produces the same exit code
and output.
