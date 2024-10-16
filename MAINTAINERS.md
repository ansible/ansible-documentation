# Maintainers guide

Find details about maintaining the `ansible-documentation` repository.
Note that maintainers have privileged access to the repository to perform special functions such as branching for new versions and preparing Ansible documentation for publishing.
If you're interested in becoming a maintainer, or want to get in touch with us, please join us on Matrix at [#docs:ansible.im](https://matrix.to/#/#docs:ansible.im).
We have weekly meetings on Matrix every Tuesday.
See [the Ansible calendar](https://forum.ansible.com/upcoming-events) for meeting details.

## Branching for new stable versions

The branching strategy for this repository mirrors the [`ansible/ansible`](https://github.com/ansible/ansible) repository.
When a new `stable-*` branch is created in the core repository, a corresponding branch in the `ansible-documentation` repository needs to be created.
There are various other changes that should occur around the same time that the new stable branch is cut.

### Creating stable branches

Create new stable branches as follows:

```bash
# Make sure your checkout is up to date.
git fetch upstream

# Create a new stable branch against the devel branch.
git checkout -b stable-2.18 upstream/devel

# Push the new stable branch to the repository.
git push upstream stable-2.18
```

After the new stable branch is created, the following changes should be committed as pull requests to the new stable branch:

* Update the core branch in the `docs/ansible-core-branch.txt` file.
* Remove devel-only tooling.
* Update Python versions in the support matrix.

### Updating the core branch

The script that grafts portions of the core repository uses the `docs/ansible-core-branch.txt` file to specify which branch to clone.
When a new stable branch is created, modify the file so that it specifies the correct version.

```bash
sed -i 's/devel/stable-2.18/g' docs/ansible-core-branch.txt
```

### Removing devel-only tooling

There are some scripts and other tooling artefacts that should be on the `devel` branch only.
After creating a new stable branch, remove the appropriate files and references.

```bash
# Remove the following workflow files, the tagger script, and tagger requirements.
git rm -r .github/workflows/pip-compile-dev.yml .github/workflows/pip-compile-docs.yml .github/workflows/reusable-pip-compile.yml .github/workflows/tag.yml hacking/tagger tests/tag.*
```

Next, remove references to the tagger dependencies as follows:

1. Remove the reference from the typing input file.

   ```bash
   sed -i '/-r tag.in/d' tests/typing.in
   ```

2. Clean up the typing lockfile.

   ```bash
   nox -s pip-compile -- --no-upgrade
   ```

3. Open `noxfile.py` and remove `"hacking/tagger/tag.py",` from the `LINT_FILES` tuple.

### Update Python versions in the support matrix

The minimum supported Python version changes with each Ansible core version.
This requires an update to the support matrix documentation after a new stable branch is created to reflect the appropriate Control Node Python versions.

Uncomment the new stable version from the `ansible-core support matrix` section in the `docs/docsite/rst/reference_appendices/release_and_maintenance.rst` file.
Submit a PR with the changes and request a core team review.

### Updating the tagger script

Update the list of active branches in the `hacking/tagger/tag.py` script on the `devel` branch.
Add the new stable branch and remove the lowest version from the `DEFAULT_ACTIVE_BRANCHES` tuple.

### Workflow Schedules

| Workflow | Schedule | Cron |
| :------- | :------- | :--- |
| [Build Package Docs](.github/workflows/build-package-docs.yaml) | Daily at 05: 17 | `17 5 * * *` |
| [CI](.github/workflows/ci.yaml) | Daily at 07:23 | `23 7 * * *`|
| [Pip Compile Dev](.github/workflows/pip-compile-dev.yml)| Weekly, Sunday at 00:00 | `0 0 * * 0`|
| [Pip Compile Docs](.github/workflows/pip-compile-docs.yml)| Weekly, Sunday at 00:00 | `0 0 * * 0`|
| [Tag](.github/workflows/tag.yml) | Hourly | `0 * * * *`|