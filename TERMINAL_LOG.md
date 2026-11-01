PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment\terraform> python -m pytest tests/test_access_control.py -v
=============================================== test session starts ================================================
platform win32 -- Python 3.12.5, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\dell\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment\terraform
collected 0 items                                                                                                   

============================================== no tests ran in 0.05s ===============================================
ERROR: file or directory not found: tests/test_access_control.py

PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment\terraform> cd ..
PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment> python -m pytest tests/test_access_control.py -v
=============================================== test session starts ================================================
platform win32 -- Python 3.12.5, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\dell\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment
collected 0 items                                                                                                   

============================================== no tests ran in 0.11s ===============================================
PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment> python -m pytest tests/test_access_control.py -v
=============================================== test session starts ================================================
platform win32 -- Python 3.12.5, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\dell\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment
collected 5 items                                                                                                   

tests/test_access_control.py::test_same_landlord_account_access_allowed PASSED                                [ 20%]
tests/test_access_control.py::test_cross_landlord_account_access_denied PASSED                                [ 40%]
tests/test_access_control.py::test_access_denied_when_tenant_not_found PASSED                                 [ 60%]
tests/test_access_control.py::test_access_denied_when_property_not_found PASSED                               [ 80%]
tests/test_access_control.py::test_access_denied_when_landlord_account_missing PASSED                         [100%]

================================================ 5 passed in 0.30s =================================================
PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment> python scripts/cost_tag_check.py fixtures/plan.json
Missing required tag 'landlord_account_id': aws_lambda_function.mls_feed_sync
Missing required tag 'landlord_account_id': aws_s3_bucket.listing_media
PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment> python -m pytest tests/test_cost_tag_check.py -v
=============================================== test session starts ================================================
platform win32 -- Python 3.12.5, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\dell\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment
collected 3 items                                                                                                   

tests/test_cost_tag_check.py::test_fixture_flags_resources_missing_landlord_tag PASSED                        [ 33%]
tests/test_cost_tag_check.py::test_check_is_idempotent PASSED                                                 [ 66%]
tests/test_cost_tag_check.py::test_check_is_generic_and_skips_noop_and_delete_changes PASSED                  [100%]

================================================ 3 passed in 0.18s =================================================
PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment> git branch
* main
PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment> git checkout -b platform-assignment

Switched to a new branch 'platform-assignment'
PS C:\Users\dell\Desktop\interview\Tacnique_assignment\haven-platform-assessment> git status
On branch platform-assignment
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   B0.md
        modified:   B1.md
        modified:   DESIGN_NOTES.md
        modified:   app/access_control.py
        modified:   scripts/cost_tag_check.py
        modified:   tests/test_access_control.py
        modified:   tests/test_cost_tag_check.py
