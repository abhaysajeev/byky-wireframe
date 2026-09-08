"""Module 2 -- Human Resources (HRMS) screens.

Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core.views import BykyScreenView
from apps.byky_core import refdata, seed
from apps.byky_cms import data as cms_data

from . import data


class HrmsScreenView(BykyScreenView):
    """Reference lists the HRMS dropdowns need."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "branches_list": cms_data.branches(),
                "states_list": cms_data.states(),
                "countries_list": cms_data.countries(),
                "designations_list": data.designations(),
                "employees_list": seed.EMPLOYEES,
                "permissions": data.PERMISSIONS,
                "counts": data.counts(),
                "not_captured": data.NOT_CAPTURED,
                "nationalities_list": refdata.NATIONALITIES,
            }
        )
        return context


class PersonalDataView(HrmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employees = data.employees()
        for i, e in enumerate(employees):
            e["json_id"] = f"scr-record-employee-{i}"
            e["fields_json"] = {
                "emp_no": e["emp_no"],
                "name": e["name"],
                "designation": e["designation"],
            }
        context["employees"] = employees
        context["doc_expiry"] = data.document_expiry_summary(employees)
        return context


class TemporaryAddressView(HrmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["awaiting"] = data.AWAITING["addresses"]
        return context


class DesignationView(HrmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        designations = data.designations()
        for i, d in enumerate(designations):
            d["json_id"] = f"scr-record-designation-{i}"
            d["fields_json"] = {
                "code": d["code"],
                "title": d["title"],
                "description": "" if d["description"] == data.SHORT else d["description"],
                "rank": d["rank"],
            }
        context["designations"] = designations
        return context


class GradeView(HrmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["awaiting"] = data.AWAITING["grades"]
        return context


class BlockUnblockView(HrmsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "awaiting": data.AWAITING["block_log"],
                "reasons": data.BLOCK_REASONS,
            }
        )
        return context


class HrmsPrivilegeView(HrmsScreenView):
    ROLES = ["SuperAdmin", "HR Manager", "Branch Manager", "Administrative Supervisor"]

    # Access, Create, Read, Update, Approve, Block Staff -- per the FSD 2.6 wireframe.
    SCREENS = [
        ("Employee Personal Data", [1, 1, 1, 1, 1, 0]),
        ("Employee Temporary Address", [1, 1, 1, 1, 0, 0]),
        ("Employee Designation Master", [1, 1, 1, 1, 0, 0]),
        ("Employee Grade Master", [1, 0, 1, 0, 0, 0]),
        ("Employee Block / Unblock", [1, 0, 1, 0, 1, 1]),
        ("HRMS Privileges", [1, 0, 1, 0, 0, 0]),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "roles": self.ROLES,
                "screens": [
                    {"name": n, "perms": [bool(x) for x in p]} for n, p in self.SCREENS
                ],
            }
        )
        return context
