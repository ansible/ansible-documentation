import subprocess
from pathlib import Path

import yaml
from docutils import nodes
from jinja2 import Template
from sphinx.transforms import Transform


class EOLVersionCheck(Transform):
    # pylint: disable=too-few-public-methods
    default_priority = 999

    def apply(self):
        env = self.document.settings.env
        app = env.app

        if app.tags.has("core"):
            build_type = "core"
        elif app.tags.has("ansible"):
            build_type = "package"
        else:
            return

        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
            ).strip()
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e}")
            return

        yaml_path = Path(env.srcdir).parent / "versions.yaml"
        template_path = Path(env.srcdir).parent / ".templates" / "eol_banner.html"

        with open(yaml_path, "r", encoding="utf-8") as f:
            versions = yaml.safe_load(f)

        with open(template_path, "r", encoding="utf-8") as f:
            template = Template(f.read())

        if branch in versions[build_type]["eol"]:
            banner_html = template.render()
            banner = nodes.raw("", banner_html, format="html")
            self.document.insert(0, banner)


def setup(app):
    app.add_transform(EOLVersionCheck)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
