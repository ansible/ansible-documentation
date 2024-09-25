# How to Contribute

The ansible-documention project is [GPL-3.0 licensed](COPYING) and accepts contributions through
GitHub pull requests.

## Certificate of Origin

By contributing to ansible-documentation, you agree to the Developer Certificate of
Origin (DCO). This document was created by the Linux Kernel community and is a
simple statement that you, as a contributor, have the legal right to make the
contribution. See the [DCO](DCO) file for details.

## Backport labels

This repository has `stable-<MAJOR>.<MINOR>` branches to correspond to each
ansible-core major release.
ansible-documentation commmitters can add `backport-<MAJOR>.<MINOR>` labels to
pull requests so the [Patchback bot] will automatically create backport pull
requests after the original PR is merged.
Small fixes or cleanups should at least be backported to the latest
stable branch.
If a PR should stay on the `devel` and not be backported—for example, if the
documentation update addresses an ansible-core change that only occurred on the
ansible-core development branch—maintainers should instead add the
`no_backport` label.

[Patchback bot]: https://github.com/apps/patchback

## Merging pull requests

This repository has two ways to apply pull requests:
`Squash and merge` and `Create a merge commit`.
`Squash and merge` squashes all of the commits from the PR's base branch into a
single commit and then applies that commit on top of the target branch in the
upstream ansible-documentation repository.
`Create a merge commit` uses `git merge` which preserves the entire commit
history from the base branch.
This may not be desired if, for example, there are a lot of fixup commits with
nondescriptive commit messages.
For other more complex changes—especially those that involve the docs build
scripts or other tooling code—it may be desirable to preserve the full commit
history to keep logical changes separated and avoid clobbering useful metadata
so the Git history remains useful in the future. The maintainer who merges the
PR can select the merge mode through the dropdown menu next to the green merge
button.
Generally, maintainers should apply PRs using `Squash and merge`.
`Create a merge commit` should be used if the PR author added the
`merge_commit` label or the maintainer otherwise assesses that merge mode makes
sense for the change in question.
