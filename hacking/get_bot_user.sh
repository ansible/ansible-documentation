#!/usr/bin/bash -x

# Set Github committer to a bot user

set -euo pipefail

bot="${1}"
name="${2-${1}}"
path="https://api.github.com/users/${bot}%5Bbot%5D"
user_id="$(curl -sS "${path}" | jq -r .id)"
GIT="${GIT:-git}"

${GIT} config user.name "${name}"
${GIT} config user.email "${user_id}+${bot}@users.noreply.github.com"
