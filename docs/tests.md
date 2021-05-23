# Test Report

*Report generated on 23-May-2021 at 15:39:41 by [pytest-md]*

[pytest-md]: https://github.com/hackebrot/pytest-md

## Summary

44 tests ran in 8.34 seconds

- 33 passed
- 11 skipped

## 33 passed

### tests/test_changelog.py

`test_write_new_changelog` 0.00s

`test_replace_sha_with_commit_link` 0.00s

### tests/test_cli.py

`test_version` 0.00s

### tests/test_init.py

`test_init_prompts_for_auth_token_and_writes_tool_config` 0.29s

`test_init_finds_auth_token_in_environment` 0.04s

### tests/test_packaging.py

`test_build_distributions` 0.00s

`test_install_package` 0.00s

`test_upload_package` 0.00s

`test_install_from_pypi` 1.30s

### tests/test_probe.py

`test_probe_project` 0.01s

`test_has_binary` 0.00s

`test_has_no_binary` 0.00s

`test_has_test_runner` 0.00s

`test_accepts_readme` 0.00s

`test_refuses_readme` 0.00s

`test_fails_for_missing_readme` 0.00s

### tests/test_publish.py

`test_publish_no_staged_release` 0.07s

`test_publish` 0.69s

### tests/test_repository.py

`test_repository_parses_remote_url` 0.03s

`test_repository_parses_versions` 0.02s

`test_latest_version` 0.05s

### tests/test_shell.py

`test_handle_dry_run` 0.01s

`test_handle_dry_run_true` 0.00s

### tests/test_stage.py

`test_stage_draft` 0.33s

`test_stage` 0.41s

`test_stage_discard` 0.40s

`test_stage_discard_nothing_staged` 0.07s

### tests/test_status.py

`test_status` 0.13s

`test_status_with_changes` 0.27s

### tests/test_util.py

`test_extract` 0.00s

`test_extract_arguments` 0.00s

### tests/test_vcs.py

`test_commit_version_change` 0.01s

`test_tag_and_push` 0.01s

## 11 skipped

### tests/test_attributes.py

`test_extract_attribute` 0.00s

`test_replace_attribute` 0.00s

`test_replace_attribute_dry_run` 0.00s

`test_has_attribute` 0.00s

### tests/test_changelog.py

`test_generate_changelog` 0.00s

### tests/test_vcs.py

`test_github_release` 0.00s

`test_upload_release_distributions` 0.00s

`test_signed_tag` 0.00s

### tests/test_version.py

`test_increment` 0.00s

`test_current_version` 0.00s

`test_get_new_version` 0.00s
