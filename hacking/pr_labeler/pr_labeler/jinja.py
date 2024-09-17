# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Utilities for Jinja2 templating
"""

from __future__ import annotations

from typing import Any, cast

from jinja2 import Environment, PackageLoader, StrictUndefined, select_autoescape

JINJA2_ENV = Environment(
    loader=PackageLoader(cast(str, __package__), "data"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    undefined=StrictUndefined,
)


def get_data_file(name: str, **kwargs: Any) -> str:
    """
    Template a data file
    """
    return JINJA2_ENV.get_template(name).render(**kwargs).rstrip("\n")
