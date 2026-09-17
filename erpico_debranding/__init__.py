# © 2026 Santiago Vásquez
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from . import controllers
from . import models
from .patches.legacy_emails import patch_legacy_emails


def post_init_hook(env):
    patch_legacy_emails(env)