# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Generic utilities
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cli_context import IssueOrPrCtx


# TODO: If we end up needing to log more things with more granularity,
# switch to something like `logging`
def log(ctx: IssueOrPrCtx, *args: object) -> None:
    print(f"{ctx.member.number}:", *args)
