"""Drawer specs for Module CMS screens.

Extracted from the screens' own markup when they moved to the shared byky
drawer, so the FSD field lists are exactly what they were -- see
apps/byky_core/drawers.py for the spec shape and how `options_from` resolves.
"""


BRANCH = {
    "drawer_id": "drawerBranch",
    "scr_name": "branch",
    "add_label": "Add Branch",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Branch Code",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "name",
                    "label": "Branch Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "company",
                    "label": "Company",
                    "kind": "select",
                    "required": True
                },
                {
                    "id": "country",
                    "label": "Country",
                    "kind": "select",
                    "required": True,
                    "options_from": "countries_list",
                    "option_key": "name"
                },
                {
                    "id": "state",
                    "label": "State",
                    "kind": "select",
                    "required": True,
                    "options_from": "states_list",
                    "help": "Choose a country first to narrow this list. Drives which fare plans and RFID gate rules this branch inherits.",
                    "option_key": "name"
                },
                {
                    "id": "location",
                    "label": "Location",
                    "kind": "select",
                    "required": True,
                    "options_from": "states_list",
                    "option_key": "name"
                },
                {
                    "id": "branch_type",
                    "label": "Branch Type",
                    "kind": "select",
                    "required": True,
                    "options_from": "branch_types_list"
                },
                {
                    "id": "hotel_commission",
                    "label": "Hotel Commission %",
                    "kind": "number",
                    "required": False,
                    "help": "Enabled only when Is Hotel is checked."
                },
                {
                    "id": "is_hotel",
                    "label": "",
                    "kind": "checkbox",
                    "required": False,
                    "enables": "hotel_commission"
                }
            ]
        }
    ]
}

COUNTRY = {
    "drawer_id": "drawerCountry",
    "scr_name": "country",
    "add_label": "Add Country",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Country Code",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "name",
                    "label": "Country Name",
                    "kind": "text",
                    "required": True
                }
            ]
        }
    ]
}

DEPARTMENT = {
    "drawer_id": "drawerDepartment",
    "scr_name": "department",
    "add_label": "Add Department",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Short Code",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "name",
                    "label": "Department Name",
                    "kind": "text",
                    "required": True
                }
            ]
        }
    ]
}

LOCATION = {
    "drawer_id": "drawerLocation",
    "scr_name": "location",
    "add_label": "Add Location",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Location Code",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "name",
                    "label": "Location Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "country",
                    "label": "Country",
                    "kind": "select",
                    "required": True,
                    "options_from": "countries_list",
                    "option_key": "name"
                },
                {
                    "id": "state",
                    "label": "State",
                    "kind": "select",
                    "required": True,
                    "options_from": "states_list",
                    "help": "Choose a country first to narrow this list.",
                    "option_key": "name"
                },
                {
                    "id": "landmark",
                    "label": "Landmark",
                    "kind": "text",
                    "required": False
                }
            ]
        }
    ]
}

MAPPING = {
    "drawer_id": "drawerMapping",
    "scr_name": "mapping",
    "add_label": "Add Mapping",
    "title_field": "branch",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "branch",
                    "label": "Branch",
                    "kind": "select",
                    "required": True,
                    "options_from": "branches_list",
                    "option_key": "name"
                },
                {
                    "id": "department",
                    "label": "Department",
                    "kind": "select",
                    "required": True
                },
                {
                    "id": "authority",
                    "label": "Leave Sanction Authority",
                    "kind": "multiselect",
                    "required": True,
                    "placeholder": "Select one or more",
                    "options_from": "employees",
                    "help": "More than one person can be authorised to sanction leave for this branch.",
                    "option_key": "name"
                },
                {
                    "id": "approvers",
                    "label": "Request Approval",
                    "kind": "multiselect",
                    "required": True,
                    "placeholder": "Select one or more",
                    "options_from": "employees",
                    "help": "Who can approve requests raised against this branch-department mapping.",
                    "option_key": "name"
                }
            ]
        }
    ]
}

STATE = {
    "drawer_id": "drawerState",
    "scr_name": "state",
    "add_label": "Add State",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "country",
                    "label": "Country",
                    "kind": "select",
                    "required": True,
                    "options_from": "countries",
                    "option_key": "name"
                },
                {
                    "id": "code",
                    "label": "State Code",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "name",
                    "label": "State Name",
                    "kind": "text",
                    "required": True
                }
            ]
        }
    ]
}

STATION = {
    "drawer_id": "drawerStation",
    "scr_name": "station",
    "add_label": "Add Station Address",
    "title_field": "station_no",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "station_no",
                    "label": "Station No",
                    "kind": "text",
                    "required": True,
                    "placeholder": "ST001",
                    "lock_on_edit": True
                },
                {
                    "id": "branch",
                    "label": "Branch",
                    "kind": "select",
                    "required": True,
                    "options_from": "branches_list",
                    "option_key": "name"
                },
                {
                    "id": "state",
                    "label": "State",
                    "kind": "select",
                    "required": True,
                    "options_from": "states_list",
                    "option_key": "name"
                },
                {
                    "id": "address",
                    "label": "Address",
                    "kind": "textarea",
                    "required": False
                },
                {
                    "id": "latitude",
                    "label": "Latitude",
                    "kind": "number",
                    "required": True,
                    "placeholder": "0.000000",
                    "help": "-90 to +90"
                },
                {
                    "id": "longitude",
                    "label": "Longitude",
                    "kind": "number",
                    "required": True,
                    "placeholder": "0.000000",
                    "help": "-180 to +180"
                },
                {
                    "id": "contact_no",
                    "label": "Contact No",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "",
                    "label": "Station Image",
                    "kind": "file",
                    "required": False
                }
            ]
        }
    ]
}


# template variable -> spec, for the view to resolve in one call
SPECS = {

    "drawer_branch": BRANCH,

    "drawer_country": COUNTRY,

    "drawer_department": DEPARTMENT,

    "drawer_location": LOCATION,

    "drawer_mapping": MAPPING,

    "drawer_state": STATE,

    "drawer_station": STATION,

}


def company_spec(form_sections):
    """Build the Company drawer from data.company_sections().

    Company Details is the one CMS drawer whose fields are generated rather
    than written out, so its spec is built per request instead of sitting in
    this file as a literal. Every field is a plain text input, and the section
    titles are the same four the full-page form uses, so the drawer and the
    page underneath it stay in step.
    """
    sections = []
    for i, s in enumerate(form_sections):
        fields = []
        if i == 0:
            fields.append({
                "id": "logo", "label": "Company Logo", "kind": "file",
                "required": False,
                "help": "PNG, JPG or SVG · square, at least 256×256px.",
            })
        for f in s["fields"]:
            fields.append({
                "id": f["key"],
                "label": f["label"],
                "kind": "text",
                "required": f["required"],
                "placeholder": f["label"],
                "help": f.get("help") or "",
                "lock_on_edit": f["key"] == "code",
                "width": f.get("span") or 6,
            })
        sections.append({"title": s["label"], "fields": fields})
    return {
        "drawer_id": "drawerCompany",
        "scr_name": "company",
        "add_label": "Add Company",
        "title_field": "name",
        "sections": sections,
    }
