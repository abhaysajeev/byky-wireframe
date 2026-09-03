"""Declarative screen specs.

Modules 4-16 are overwhelmingly the same shape: a filter bar, a data grid, and a
create/edit drawer. Rather than hand-writing ~70 near-identical templates (which is
how spacing and markup drift creeps in), each screen declares its FSD fields here
and renders through byky/generic_screen.html.

Bespoke templates stay for screens that genuinely differ -- the CMS shift matrix,
the block/unblock console, the privilege matrix, the dashboard.
"""


# --- filter bar -------------------------------------------------------------
def text_filter(placeholder):
    return {"kind": "text", "placeholder": placeholder}


def date_filter(placeholder):
    return {"kind": "date", "placeholder": placeholder}


def select_filter(label, options=(), source=None):
    """`source` names a context list (branches_list, categories_list, ...)."""
    return {"kind": "select", "label": label, "options": list(options), "source": source}


# --- grid columns -----------------------------------------------------------
def col(label, key, align="", style=""):
    """style: '' | 'strong' | 'code' | 'muted' | 'badge' | 'status'"""
    return {"label": label, "key": key, "align": align, "style": style}


# --- form fields ------------------------------------------------------------
def field(fid, label, kind="text", required=False, placeholder="", options=(),
          source=None, width=6, help_text=""):
    return {
        "id": fid, "label": label, "kind": kind, "required": required,
        "placeholder": placeholder, "options": list(options), "source": source,
        "width": width, "help": help_text,
    }


def section(title, fields):
    return {"title": title, "fields": fields}


# --- whole screen -----------------------------------------------------------
def screen(filters=(), columns=(), sections=(), add_label=None, drawer_id=None,
           wide=False, row_actions=("Edit", "Delete"), kpis=()):
    return {
        "filters": list(filters),
        "columns": list(columns),
        "sections": list(sections),
        "add_label": add_label,
        "drawer_id": drawer_id or "offcanvasAdd",
        "wide": wide,
        "row_actions": list(row_actions),
        "kpis": list(kpis),
    }
