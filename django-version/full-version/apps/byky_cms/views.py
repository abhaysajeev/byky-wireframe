"""Module 1 -- Company Management (CMS) screens.

Each view extends BykyScreenView so the FSD identity (screen number, tier, legacy
page) stays in context and the page header renders consistently.

Wireframe phase: no writes, no CRUD, no API. Forms submit nowhere.
"""

from apps.byky_core.views import BykyScreenView
from apps.byky_core import drawers as core_drawers, geo, seed
from apps.byky_ims import data as ims_data

from . import data, drawers


class CmsScreenView(BykyScreenView):
    """Adds the CMS reference lists every screen's dropdowns need."""

    drawer_specs = drawers.SPECS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "states_list": data.states(),
                "countries_list": data.countries(),
                "branches_list": data.branches(),
                "departments_list": data.departments(),
                "permissions": data.PERMISSIONS,
            }
        )
        return context


class CompanyDetailsView(CmsScreenView):
    """No company is registered yet on this screen -- the list shows the empty
    state and the Company Record form below is blank, ready for first-time
    entry. This is scoped to this page only: data.company() (and the fleet,
    station and workforce data every other screen uses) is untouched."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sections = data.company_sections({})
        completeness = data.company_completeness(sections)
        context.update(
            {
                "companies": [],
                "form_sections": sections,
                "completeness": completeness,
                "active_count": 0,
                "form_active_default": True,
                "company_logo": "",
                # generated, not a literal spec -- see drawers.company_spec
                "drawer_company": drawers.company_spec(sections),
            }
        )
        return context


class CountryStateView(CmsScreenView):
    """FSD 1.2 -- Tier A, tabbed dual grid. Countries and their states/emirates,
    each with its own Add drawer, on the shared byky-screen.css/js base."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        countries = [dict(c) for c in data.countries()]
        states = [dict(s) for s in data.states()]

        for i, c in enumerate(countries):
            c["json_id"] = f"scr-record-country-{i}"
            c["fields_json"] = {"name": c["name"], "code": c["code"], "active": c["active"]}

        for i, s in enumerate(states):
            s["json_id"] = f"scr-record-state-{i}"
            s["fields_json"] = {
                "name": s["name"],
                "code": s["code"],
                "country": s["country"],
                "active": s["active"],
            }

        total_branches = sum(s["branches"] for s in states)
        total_fleet = sum(s["fleet"] for s in states)
        context.update(
            {
                "countries": countries,
                "states": states,
                "total_branches": total_branches,
                "total_fleet": total_fleet,
                # Company equipment, not vehicles -- the count the Asset
                # Management register holds, which these tiles link through to.
                # Zero until an equipment inventory is supplied; adding
                # branches and fleet together would put a number here that
                # counts nothing anyone can go and look at.
                "total_assets": ims_data.asset_counts()["registered"],
            }
        )
        return context


class LocationView(CmsScreenView):
    """FSD 1.3 -- Tier A. No source data (CLAUDE.md 12); the grid shows its
    column headers with the awaiting-data state in the body, on the shared
    byky-screen.css/js base."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["awaiting"] = data.AWAITING["locations"]
        return context


class BranchView(CmsScreenView):
    """FSD 1.4 -- Tier B rental station branch hubs, on the shared
    byky-screen.css/js base. All 36 rows are real stations from seed data."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = [dict(b) for b in data.branches()]
        for i, b in enumerate(rows):
            b["json_id"] = f"scr-record-branch-{i}"
            b["vehicles_json_id"] = f"scr-vehicles-branch-{i}"
            b["vehicles_json"] = [
                {
                    "number": v["number"],
                    "rfid_epc": v["barcode"],  # the client's Barcode column is the RFID tag EPC
                    "nfc_id": data.NOT_CAPTURED,  # no NFC data in the client files
                    "category": v["category"],
                    "vtype": v["vtype"],
                }
                for v in seed.vehicles_at(b["station_code"])
            ]
            b["fields_json"] = {
                "code": b["code"],
                "name": b["name"],
                "company": b["company"],
                "country": data.country_of_state(b["location"]),
                "state": b["location"],
                "location": b["location"],
                "branch_type": b["branch_type"],
                "is_hotel": b["is_hotel"],
                "app_payment": b["app_payment"],
                "multi_user": b["multi_user"],
                "test_vehicle": b["test_vehicle"],
                "hotel_commission": b["hotel_commission"],
                "active": b["active"],
            }
        context.update(
            {
                "branches": rows,
                "total_fleet": sum(b["fleet"] for b in rows),
                "assets_deployed": sum(b["assets_deployed"] for b in rows),
                "ho_count": sum(1 for b in rows if b["is_ho"]),
                "inactive_count": sum(1 for b in rows if not b["active"]),
                "branch_types_list": data.BRANCH_TYPES,
                "regional_office_count": sum(1 for b in rows if b["branch_type"] == "Regional Office"),
                "regional_warehouse_count": sum(1 for b in rows if b["branch_type"] == "Regional Warehouse"),
                "branch_office_count": sum(1 for b in rows if b["branch_type"] == "Branch Office"),
                "branch_warehouse_count": sum(1 for b in rows if b["branch_type"] == "Branch Warehouse"),
            }
        )
        return context


class DepartmentView(CmsScreenView):
    """FSD 1.5. Rows are demo data -- see data._DEMO_DEPARTMENTS."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = [dict(d) for d in data.departments()]
        for i, d in enumerate(rows):
            d["json_id"] = f"scr-record-department-{i}"
            d["fields_json"] = {"code": d["code"], "name": d["name"]}
        context["departments"] = rows
        context["awaiting"] = data.AWAITING["departments"]
        return context


class BranchDepartmentView(CmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "awaiting": data.AWAITING["branch_departments"],
                "employees": seed.EMPLOYEES,
            }
        )
        return context


class StationAddressView(CmsScreenView):
    """FSD 1.7 -- Tier A, on the shared byky-screen.css/js base. All 36 rows are
    real stations; GPS, address and contact have no source in the client files
    (CLAUDE.md 12) and render blank, not fabricated. The map preview uses the
    same real (if not survey-grade) coordinates as the dashboard's network map,
    drawn with the same hand-rolled SVG technique -- see byky-station-address.js."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addresses = [dict(a) for a in data.station_addresses()]
        for i, a in enumerate(addresses):
            a["json_id"] = f"scr-record-station-{i}"
            a["fields_json"] = {
                "station_no": a["station_no"],
                "branch": a["branch"],
                "state": a["state"],
                "latitude": "" if a["latitude"] == data.SHORT else a["latitude"],
                "longitude": "" if a["longitude"] == data.SHORT else a["longitude"],
                "contact_no": "" if a["contact_no"] == data.SHORT else a["contact_no"],
            }
        context.update(
            {
                "addresses": addresses,
                "map_points": geo.station_points(),
            }
        )
        return context


class StationWorkingTimeView(CmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "days": data.DAYS,
                "shifts": data.SHIFTS,
                "awaiting": data.AWAITING["working_times"],
            }
        )
        return context


class CmsPrivilegeView(CmsScreenView):
    """Tier D. Screen list comes from this module's own FSD screens."""

    ROLES = ["SuperAdmin", "SystemAdmin", "BranchManager", "Cashier", "Store Keeper"]

    # Access, Create, Read, Update, Print, Approve, Delete -- as granted to the
    # first role in the list. FSD 1.9 wireframe shows a partially-filled matrix.
    SCREENS = [
        ("Company Details", "CompanyManagement.aspx", [1, 1, 1, 1, 1, 1, 0]),
        ("Country & State Management", "CountryManagement.aspx", [1, 1, 1, 1, 0, 1, 0]),
        ("Location Management", "CoreLocationManagement.aspx", [1, 1, 1, 1, 0, 0, 0]),
        ("Branch Management", "BranchManagement.aspx", [1, 1, 1, 1, 0, 0, 0]),
        ("Department Management", "DepartmentManagement.aspx", [1, 1, 1, 1, 0, 0, 0]),
        ("Branch Department Mapping", "BranchDepartmentManagement.aspx", [1, 1, 1, 0, 0, 0, 0]),
        ("Station Address Mapping", "StationAddressMapping.aspx", [1, 0, 1, 0, 0, 0, 0]),
        ("Branch Working Time", "StationWorkingTime.aspx", [1, 0, 1, 1, 0, 0, 0]),
        ("CMS Privilege Management", "CMSPrivilegeManagement.aspx", [1, 0, 1, 0, 0, 0, 0]),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "roles": self.ROLES,
                "screens": [
                    {"name": n, "legacy_page": p, "perms": [bool(x) for x in perms]}
                    for n, p, perms in self.SCREENS
                ],
            }
        )
        return context
