"""Module 1 -- Company Management (CMS) screens.

Each view extends BykyScreenView so the FSD identity (screen number, tier, legacy
page) stays in context and the page header renders consistently.

Wireframe phase: no writes, no CRUD, no API. Forms submit nowhere.
"""

from apps.byky_core.views import BykyScreenView
from apps.byky_core import geo, seed

from . import data


class CmsScreenView(BykyScreenView):
    """Adds the CMS reference lists every screen's dropdowns need."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "states_list": data.states(),
                "countries_list": data.countries(),
                "branches_list": data.branches(),
                "permissions": data.PERMISSIONS,
            }
        )
        return context


class CompanyDetailsView(CmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"company": data.company(), "companies": [data.company()]})
        return context


class CountryStateView(CmsScreenView):
    pass


class CoreLocationView(CmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["awaiting"] = data.AWAITING["core_locations"]
        return context


class BranchView(CmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.branches()
        context.update(
            {
                "branches": rows,
                "total_fleet": sum(b["fleet"] for b in rows),
                "ho_count": sum(1 for b in rows if b["is_ho"]),
                "pending": sum(1 for b in rows if b["status"] == "Pending"),
            }
        )
        return context


class DepartmentView(CmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "addresses": data.station_addresses(),
                "map_data": geo.station_points(),
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
        ("Core Location Management", "CoreLocationManagement.aspx", [1, 1, 1, 1, 0, 0, 0]),
        ("Branch Management", "BranchManagement.aspx", [1, 1, 1, 1, 0, 0, 0]),
        ("Department Management", "DepartmentManagement.aspx", [1, 1, 1, 1, 0, 0, 0]),
        ("Branch Department Mapping", "BranchDepartmentManagement.aspx", [1, 1, 1, 0, 0, 0, 0]),
        ("Station Address Mapping", "StationAddressMapping.aspx", [1, 0, 1, 0, 0, 0, 0]),
        ("Station Working Time", "StationWorkingTime.aspx", [1, 0, 1, 1, 0, 0, 0]),
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
