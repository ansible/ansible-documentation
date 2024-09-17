# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Constants for the tagging script
"""

from __future__ import annotations

from pathlib import Path

from codeowners import OwnerTuple

OWNER = "ansible"
REPO = "ansible-documentation"
LABELS_BY_CODEOWNER: dict[OwnerTuple, list[str]] = {
    ("TEAM", "@ansible/steering-committee"): ["sc_approval"],
}
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
CODEOWNERS = (ROOT / ".github/CODEOWNERS").read_text("utf-8")
NEW_CONTRIBUTOR_LABEL = "new_contributor"
