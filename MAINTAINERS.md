# Maintainers guide

Find details about maintaining the `ansible-documentation` repository.
Note that maintainers have privileged access to the repository to perform special functions such as branching for new versions and preparing Ansible documentation for publishing.
If you're interested in becoming a maintainer, or want to get in touch with us, please join us on [Ansible Forum](https://forum.ansible.com/tag/documentation/7) and Matrix at [#docs:ansible.im](https://matrix.to/#/#docs:ansible.im).

## Triaging new issues and pull requests

Regular triage of new issues and pull requests is a core maintainer activity.

### Triage labels

[`ansible-documentation-bot`](https://github.com/apps/ansible-documentation-bot/) is a GitHub App that labels new issues and pull requests as well as performing other workflow activities, such as creating PRs for the porting guide.

For the purpose of triage, `ansible-documentation-bot` adds the following labels to issues and PRs:

- `needs_triage` indicates that a maintainer, or other contributor, should do an initial review and assessment.
- `sc_approval` indicates that a pull request MUST be reviewed and approved by the Ansible community steering committee before merging.
  This label applies to files specified in the [.github/CODEOWNERS](.github/CODEOWNERS) file as owned by the `@ansible/steering-committee` group.

### Triaging issues and pull requests

For issues and pull requests with the `needs_triage` label, triage involves the following steps:

1. Ensure compliance with the following policies where appropriate:

    - [Ansible code of conduct](https://docs.ansible.com/projects/ansible/devel/community/code_of_conduct.html)
    - [Ansible AI policy](https://docs.ansible.com/projects/ansible/devel/community/ai_policy.html)
    - [Ansible security vulnerability reporting policy](https://docs.ansible.com/projects/ansible/devel/community/security_policy.html#reporting-a-vulnerability)

1. Add any other labels as necessary, such as:

    - `core_approval` indicates an issue needs Ansible core team attention.
    - `sc_approval` indicates approval is required by the Ansible community steering committee.
    - `techreview` indicates that technical review is needed from an appropriate subject matter expert (SME).
      If you aren't sure who is the appropriate SME, it's usually bcoca.
    - `easy fix` and `good first issue` indicate good opportunities for new contributors, as outlined on the [How can I help?](https://docs.ansible.com/projects/ansible/latest/community/how_can_I_help.html#review-and-submit-pull-requests) page.
    - `help wanted` indicates when help is needed or if the issue is available for investigation by any interested contributor.
    - `blocked` indicates change is blocked on another task.
    - `needs_info` indicates that information in the issue body is insufficient or unclear.
      Before adding the `needs_info` label, you should add a comment to ask for clarification and explain why information is needed.

1. Mention related groups and/or contributors if required, for example:

    - `@ansible/community-docs-maintainers`
    - `@ansible/steering-committee`
    - `@ansible/community-team-internal`
    - `@ansible/release-management-wg`

1. When triage is complete, remove the `needs_triage` label.

### Merging and backporting pull requests

Review and merge PRs where you're certain the changes are OK.
If you aren't sure, ask the community on the [Ansible Forum](https://docs.ansible.com/projects/ansible/devel/community/communication.html#forum) and/or in appropriate [Matrix channels](https://docs.ansible.com/projects/ansible/devel/community/communication.html#general-channels) to take a look.

Before merging a PR, add appropriate `backport-VER` labels that correspond to ansible-core branches.
For example, the `backport-2.22` label corresponds to the stable-2.22 branch.
When the PR is merged, the `backport-VER` labels prompt the patchback bot to open backport PRs against relevant branches.

Here are some guidelines for backporting PRs:

- The person who merges a PR is responsible for backporting it to all relevant branches and ensuring the backport PRs are merged.
- Check that the git diff on each backport PR matches the original PR.
- Merged PRs should be backported to all branches where the documentation change is relevant.
  However backporting to older stable branches is best effort.
  If changes have conflicts on older branches and do not backport cleanly, it is generally acceptable to leave them.
  You can manually backport changes by following the instructions that the patchback bot provides in the original PR.
- Wait until the backport PRs pass all CI checks before merging.
  There are typically slight differences between branches that can unexpectedly result in CI failures.
  If this happens, you'll need to push the necessary fix to the branch that the patchback bot created.

#### Backport labels

Changes merged to the `devel` branch are typically backported to the previous three stable versions of ansible-core.
For example, if `devel` corresponds to an unreleased 2.23 version, changes should be backported to `2.22`, `2.21`, and `2.20`.

Generally each new `backport-VER` label should be created when a new stable branch is cut.

When a stable branch reaches EOL, the `backport-VER` label should be deleted.
However this usually does not happen immediately because it might be necessary to do a final build of the EOL stable branch before the next version of the Ansible community package is released.
A good rule of thumb is to delete the `backport-VER` label when the EOL stable branch is removed from the `pip-compile-dev` workflow

## Requesting review from legal

Any modifications to the `DCO` or `COPYING` file must be reviewed and approved by the Red Hat open-source legal team.
Send an email with the request to `opensource-legal@redhat.com` with `ansible-community-team@redhat.com` on copy.

## Reviewing and merging dependency refreshes

At the start of each week the `.github/workflows/pip-compile-*` workflows run.
These workflows bump dependencies and create pull requests such as [PR 2842](https://github.com/ansible/ansible-documentation/pull/2842).

PRs to bump dependencies should be merged in a timely fashion.
The documentation repo categorizes dependencies into separate requirements files.
The weekly schedule for workflow runs also ensures fewer dependencies are bumped at a time.
This granularity and isolation helps us detect incompatibilities and issues that a new version of a dependency might introduce.

When reviewing PRs to refresh dependencies, look at the files changed and note the name of the requirements file.
This corresponds to a check in CI; for example `tests/static.txt` contains the dependencies for the `nox / Run nox static session` check.

In general, CI check will emit errors or warnings if the dependency refresh introduces an issue of some kind.
So basically, during review, expand the CI checks and look for problems in the output of the relevant steps.
If there are no errors, warnings or other messages and the step has run successfully, the dependency bump should be fine to approve and merge.

In most cases, when a dependency refresh causes an issue, you probably need to adjust something in the appropriate session in `noxfile.py`.
For example, [PR 1172](https://github.com/ansible/ansible-documentation/pull/1172) bumped the version of `ruff` which resulted in a warning because the `static` session included a deprecated command.
To fix the issue, [PR 1191](https://github.com/ansible/ansible-documentation/pull/1191) updated the `ruff` command and was merged before [PR 1172](https://github.com/ansible/ansible-documentation/pull/1172).

## Updating scheduled builds for new major Ansible versions

When a new major Ansible version is released, you need to update the latest version in the scheduled docs build.

1. Open `.github/workflows/build-latest-docs.yaml` for editing.
2. Modify the `repository-branch` and `ansible-package-version` fields in the `build-package-docs` and `deploy-package-docs` jobs, for example:

   ```yaml
   # Values for the Ansible 11 release
   with:
     ansible-package-version: '11'
     repository-branch: 'stable-2.18'

   # Values for the Ansible 12 release
   with:
     ansible-package-version: '12'
     repository-branch: 'stable-2.19'
   ```

## Branching for new major stable versions

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
git rm -r .github/workflows/pip-compile-*.yml .github/workflows/reusable-pip-compile.yml .github/workflows/tag.yml .github/workflows/build-*-docs.yaml .github/workflows/reusable-*-docs.yaml hacking/tagger tests/tag.*
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

### Updating the pip compile dev workflow

Update the `.github/workflows/pip-compile-dev.yml` workflow so that it includes the new stable branch and drops the oldest branch.

### Update Python versions in the support matrix

The minimum supported Python version changes with each Ansible core version.
This requires an update to the support matrix documentation after a new stable branch is created to reflect the appropriate Control Node Python versions.

Uncomment the new stable version from the `ansible-core support matrix` section in the `docs/docsite/rst/reference_appendices/release_and_maintenance.rst` file.
Submit a PR with the changes and request a core team review.

### Updating the tagger script

Update the list of active branches in the `hacking/tagger/tag.py` script on the `devel` branch.
Add the new stable branch and remove the lowest version from the `DEFAULT_ACTIVE_BRANCHES` tuple.

## Updating the package doc builds repository

The `ansible-community/package-doc-builds` repository holds the deployed output of package doc builds.
For each version of the Ansible package that is currently supported, there needs to be a corresponding branch in the `ansible-community/package-doc-builds` repository.

Before the docs for new package version can be built on Read the Docs, someone needs to create a branch as follows:

```bash
# Make sure your checkout is up to date.
git fetch upstream

# Create the new package version branch against the devel branch.
git checkout -b 11 upstream/devel

# Push the new package version branch to the repository.
git push upstream 11
```

## Updating the package docs build workflow

The build workflow lists the Ansible package versions as input options, for example:

```yaml
options:
- devel
- '11'
- '10'
- '9'
```

After creating a new branch for the Ansible package version in the `ansible-community/package-doc-builds` repository, you should check that the build workflow lists that version as an option.
If the version is not listed, open a PR against the `devel` branch to update the workflow file.

## Maintaining Read the Docs projects

There are two Read the Docs projects associated with the `ansible-documentation` repository, as follows:

* Ansible package
* Ansible core

### Configuration files

The Ansible package and Ansible core projects use separate configuration files, as follows:

* Ansible package configuration is the `package-doc-builds` repository at [https://github.com/ansible-community/package-doc-builds/blob/devel/.readthedocs.yaml](https://github.com/ansible-community/package-doc-builds/blob/devel/.readthedocs.yaml)
* Ansible core configuration is in the `ansible-documentation` repository at [https://github.com/ansible/ansible-documentation/blob/devel/.readthedocs.yaml](https://github.com/ansible/ansible-documentation/blob/devel/.readthedocs.yaml)

> Each branch has its own Read the Docs configuration file.

Most of the time there is no need to update the Read the Docs configuration files.
The only change that should be necessary between versions is the Python version, for example:

```yaml
build:
  os: ubuntu-lts-latest
  tools:
    python: >-
      3.11
```

This Python version should match whatever version is used in the `ansible-documentation` repository to compile requirements and build the documentation.
For example, the `stable-2.18` branch uses Python 3.11.
The Python version should be also be 3.11 in the Read the Docs configuration for both Ansible package and Ansible core.
You can verify the Python version in the `pip-compile` session of the `noxfile.py` on the respective branch.

> In the Read the Docs settings, the **Build pull requests for this project** option is selected only for the Ansible core project.
> The configuration file for that project is in the `ansible-documentation` repository, which accepts pull requests.
> The `package-doc-builds` repository is used to hold generated artifacts from the build workflow and does not get pull requests.

### Updating Read the Docs for new releases

When there is a new version of the Ansible package or Ansible core, someone needs to updates the Read the Docs project.

To update the Ansible package project, do the following:

1. Ensure you have maintainer access to the project.
2. Navigate to the [package-doc-builds dashboard](https://app.readthedocs.org/projects/package-doc-builds/).
3. Select the **Add version** button and select the new version to activate, which should be a new `XX` branch.
4. Wait for the new version build to complete and then edit the main project settings.
5. From the **Default branch** drop-down, select the new version that should correspond to "latest" and save your changes.

To update the Ansible core project, do the following:

1. Ensure you have maintainer access to the project.
2. Navigate to the [ansible-core dashboard](https://app.readthedocs.org/projects/ansible-core/).
3. Select the **Add version** button and select the new version to activate, which should be a new `stable-*` branch.

### Hiding versions on Read the Docs

Hiding older versions removes them from the fly-out menu on Read the Docs as well as search results.
Older versions of the documentation that are not supported or EOL should be hidden.
It is also possible to hide doc builds before they are released to evaluate the content.
At release day, all that is needed is to toggle the switch so the build is no longer hidden and, in the case of the package docs, update the default branch for the project.

To hide versions, do the following:

1. Open the settings for the version you want to remove.
2. Select the **Hidden** option.

See [How to hide a version and keep its documentation online](https://docs.readthedocs.io/en/stable/guides/hiding-a-version.html) for more information.

## Building and deploying Ansible community documentation

Content available at [ansible.readthedocs.io/projects/ansible/](https://ansible.readthedocs.io/projects/ansible/latest/) is built and deployed from the `ansible-documentation` repository using a GitHub workflow.
This section explains how maintainers can build and deploy the Ansible package docs using that workflow.

> Details about what each job in the workflow does is beyond the scope of this maintainer guide.
> Refer to the comments in the workflow itself for more information.

### Building community documentation

The Ansible package docs build workflow allows you to run a Sphinx build with the `make webdocs` target on GitHub hosted runners.
The workflow can build from any account or org as well as from the `ansible-documentation` repository.
For instance, if you wanted to build the content of a branch in someone's fork, you can provide those details as inputs when running the workflow.

To build the docs, do the following:

1. Navigate to the [Ansible package docs build](https://github.com/ansible/ansible-documentation/actions/workflows/build-package-docs.yaml) workflow.
2. Select the **Run workflow** drop-down to open the dialog.
3. Provide the necessary inputs and then select **Run workflow**.

> If the workflow fails for any reason, the `docs-bot` posts a message in the `#docs:ansible.com` channel on Matrix.

When the workflow run is complete, you can find the output available as an artifact on the **Summary** page.
The artifact is named **package-docs-build** and contains a tarball with the generated HTML and other build assets.

### Deploying to stage

To evaluate changes from a particular branch, you can deploy the docs build to a stage environment at [https://ansible-community.github.io/package-doc-builds/](https://ansible-community.github.io/package-doc-builds/).

This stage environment is a GitHub pages deployment.
When you deploy to stage, a job in the workflow run unpacks the contents of the **package-docs-build** artifacts and pushes them to the `gh-pages` branch of the `ansible-community/package-doc-builds` repository.

To deploy to stage, do the following:

1. Follow the steps to build the docs with the `Ansible package docs build` workflow.
2. Select the **Deploy the build** option.
3. Select **test** from the **Deployment environment** drop-down.

If the build job succeeds, a member of the `community-docs-maintainers` team must review and approve the deployment.

You can find details about the workflow run, including a link to the stage deployment, from the **Summary** page of the workflow run.
Build logs are available from each job in the workflow run.

### Deploying to Read the Docs

To publish Ansible package docs to Read the Docs, do the following:

1. Ensure that the target branch exists in the `ansible-community/package-doc-builds` repository.
   For example, if you want to publish version `10` of the package docs then a branch named `10` should exist in the repository.
   The deploy job pushes the generated HTML and other build assets to that target branch.
2. Follow the steps to build the docs with the `Ansible package docs build` workflow.
3. Select the **Deploy the build** option.
4. Select **production** from the **Deployment environment** drop-down.

If the build job succeeds, a member of the `community-docs-maintainers` team must review and approve the deployment.

You can find details about the workflow run, including a link to the Read the Docs project deployment, from the **Summary** page of the workflow run.
Build logs are available from each job in the workflow run.

> The resulting documentation is available on Read the Docs only if the version is active in the `package-doc-builds` project.
> If the version is hidden in the project, that documentation will not be available in the fly-out menu or search results.

### Reviewing deployments

The `deploy-package-docs` job in the Ansible package docs build workflow uses a deployment protection rule.
This rule requires a member of the [community-docs-maintainers](https://github.com/orgs/ansible/teams/community-docs-maintainers) team to review any deployment to stage or Read the Docs.

Members of that team can do the following when they receive email notifications of pending deployments:

1. Review deployment details on the **Summary** page of the workflow run.
2. If necessary, download the **package-docs-build** artifact from the **Summary** page and then extract it to manually verify the build locally.
3. Provide comments, if necessary, and then approve or reject the deployment.

> You should always provide comments to justify deployment rejections.
