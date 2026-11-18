# How to Contribute

The ansible-documentation project is [GPL-3.0 licensed](COPYING) and accepts contributions through
GitHub pull requests.

## Certificate of Origin

By contributing to the ansible-documentation project, you agree to the Developer Certificate of
Origin (DCO).

The DCO was created by the Linux Kernel community and is a
simple statement that you, as a contributor, have the legal right to make the
contribution.
Please take time to read through the [DCO](DCO) before making your first contribution.

## Getting familiar with branches

This repository has a `devel` branch and various `stable-*` branches.

You should always target the `devel` branch as the starting point for any changes.
For example, when you create a fresh branch, make sure that it tracks `devel` as follows:

```bash
# ansible-documentation is added as a remote named upstream
git checkout -b my-docs-changes upstream/devel
```

After review and approval, changes are generally merged to `devel` and then backported to the relevant `stable-*` branches.
[Patchback bot](https://github.com/apps/patchback) takes care of the backports, though, so contributors generally don't need to be concerned with any branches other than `devel`.

Note that you might also find other branches, such as ones prefixed with `patchback`.
These branches are temporary or might belong to another contributor.
If you're a new contributor, you can simply disregard branches other than `devel` or `stable-*`.

### Stable branches

Each `stable` branch corresponds to a major release of ansible-core in this format: `stable-<MAJOR>.<MINOR>`.

If your changes apply to a specific version of ansible-core, you should add the corresponding `backport-<MAJOR>.<MINOR>` label to your pull request.
Reviewers can also add labels before merging and if you're unsure of which labels might apply, please ask in your pull request.

Here are some general guidelines for backporting changes:

- Small fixes or cleanups should be backported to the latest stable branch.
- Before merge, all PRs should have an appropriate backport label.
  Add the `no_backport` if changes are `devel` only.

## Reviewing and merging changes

We welcome and encourage collaborative reviews of all changes to this project.

If you're new to Ansible, reviewing pull requests is a good way to learn.
For automation experts, developers, and maintainers, reviewing changes to ansible-documentation is a great way to stay up to date on the latest changes.

While anyone can participate in the review process, merging changes to ansible-documentation is handled by project maintainers.
If you're interested in that process, check out the [MAINTAINERS](MAINTAINERS.md) guide.
