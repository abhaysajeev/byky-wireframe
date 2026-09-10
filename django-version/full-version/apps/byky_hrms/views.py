"""Module 2 -- Human Resources (HRMS) screens.

Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core.views import BykyScreenView
from apps.byky_core import privileges, refdata, seed
from apps.byky_cms import data as cms_data

from . import data, drawers


class HrmsScreenView(BykyScreenView):
    """Reference lists the HRMS dropdowns need."""

    drawer_specs = drawers.SPECS

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
    """Tier D -- roles list + per-role screen permission matrix. See
    apps/byky_core/privileges.py for the shared role master and defaults."""

    SLUG = "hrms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screens = privileges.module_screens(self.SLUG)
        mapped = privileges.DEFAULT_MAPPED_ROLES
        context.update(
            {
                "roles": privileges.ROLES,
                "mapped_roles": mapped,
                "admin_roles": privileges.ADMIN_ROLES,
                "screens": screens,
                "role_matrices": privileges.role_matrices(privileges.ROLES, screens, context["permissions"]),
            }
        )
        return context
