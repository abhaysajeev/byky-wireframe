"""Shared data for every module's Tier D privilege screen.

One canonical role master (the client's 8 requested roles) instead of each
module inventing its own role list. A module's privilege screen starts with
most of these roles already mapped; the two left out (PRO, Warehouse
Manager) exist purely so "+ Add Role" has something to demonstrate on
every module without a real per-module RBAC assignment to draw from --
the FSD does not specify one, so the same default applies everywhere
rather than inventing per-module distinctions that would look sourced.

Each screen's row list (module_screens) is read live from the sidebar's own
vertical_menu.json rather than a second, hand-maintained copy -- so editing
the sidebar (adding, renaming, removing a screen) is reflected here with no
other change needed.
"""

import json

from django.conf import settings

ROLES = [
    "App Admin",
    "Web Admin",
    "Manager",
    "Assistant Manager",
    "Accountant",
    "Assistant Accountant",
    "PRO",
    "Warehouse Manager",
]

# Roles treated as full-access for the default permission grant below, and
# flagged "Full Access" (vs "Custom") in every module's role list.
ADMIN_ROLES = {"App Admin", "Web Admin"}

# Held back from every module's default role list so "+ Add Role" always has
# something to add out of the box -- see module docstring.
_DEFAULT_UNMAPPED = {"PRO", "Warehouse Manager"}
DEFAULT_MAPPED_ROLES = [r for r in ROLES if r not in _DEFAULT_UNMAPPED]

_MENU_FILE = (
    settings.BASE_DIR / "templates" / "layout" / "partials" / "menu" / "vertical" / "json" / "vertical_menu.json"
)


def module_screens(slug):
    """Leaf screen names under the sidebar group with this slug.

    Read straight from vertical_menu.json -- the same file the sidebar
    itself renders from (templates/layout/bootstrap/layout_vertical.py) --
    so a privilege screen's rows can never drift from what a user actually
    sees in the menu.
    """
    try:
        menu = json.load(_MENU_FILE.open())
    except (OSError, json.JSONDecodeError):
        return []
    for item in menu.get("menu", []):
        if item.get("slug") == slug:
            return [s["name"] for s in item.get("submenu", []) if s.get("name")]
    return []


def default_perms(role, permissions):
    """A role's starting checkbox state for one screen's permission list.

    App Admin / Web Admin start fully granted; every other role starts with
    just Access + Read. Every checkbox stays editable -- this is a sensible
    starting point for the demo, not an FSD-specified matrix (none exists
    per role), so it is deliberately the same shape for every screen.
    """
    if role in ADMIN_ROLES:
        return [True for _ in permissions]
    return [p in ("Access", "Read") for p in permissions]


def role_matrices(roles, screens, permissions):
    """{role} -> its full screen x permission grid, for every role in `roles`
    (mapped or not -- the caller decides which rows/matrices to show)."""
    out = []
    for role in roles:
        perms = default_perms(role, permissions)
        out.append(
            {
                "role": role,
                "is_admin": role in ADMIN_ROLES,
                "screens": [{"name": s, "perms": list(perms)} for s in screens],
            }
        )
    return out
