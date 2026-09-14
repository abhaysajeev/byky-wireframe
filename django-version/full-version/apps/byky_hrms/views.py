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


class IncentiveView(HrmsScreenView):
    """RMS WEB APK UI.xlsx feedback -- built from the client's incentive.html
    mockup, not an FSD screen. See data.py's module note for how the
    mockup's invented user-type list maps onto real designations()."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plans = data.incentive_plans()
        for i, p in enumerate(plans):
            p["json_id"] = f"scr-record-incentive-{i}"
            p["breakdown_json_id"] = f"scr-record-incentive-{i}-breakdown"
            p["fields_json"] = {
                "code": p["code"],
                "name": p["name"],
                "user_types": p["types"],
                "breakdown_data": {r["type"]: {"target_pct": r["target_pct"], "dividend": r["dividend"]} for r in p["rows"]},
            }
            p["breakdown_view"] = [
                {"type": r["type"], "target_pct_display": f'{r["target_pct"]}%', "dividend_label": data.dividend_label(r)}
                for r in p["rows"]
            ]
        context.update(
            {
                "incentive_plans": plans,
                "incentive_counts": data.incentive_counts(plans),
                "incentive_user_types_list": data.incentive_user_types(),
            }
        )
        return context


class IncentiveBranchMappingView(HrmsScreenView):
    """RMS WEB APK UI.xlsx feedback -- built from the client's
    incentive-branch-mapping.html mockup, not an FSD screen."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branches_list = context["branches_list"]
        all_branch_names = [b["name"] for b in branches_list]
        branch_by_name = {b["name"]: b for b in branches_list}
        plans = data.incentive_plans()
        mappings = data.incentive_branch_mappings()
        for i, m in enumerate(mappings):
            m["json_id"] = f"scr-record-ibm-{i}"
            m["branches_json_id"] = f"scr-record-ibm-{i}-branches"
            m["branch_names"] = data.mapping_branch_keys(m, all_branch_names)
            m["branch_objects"] = [
                {"name": n, "location": branch_by_name[n]["location"]}
                for n in m["branch_names"] if n in branch_by_name
            ]
            m["plan"] = data.incentive_plan_by_code(m["plan_code"])
            m["expiring"] = data.is_expiring_soon(m["valid_to"])
            m["fields_json"] = {
                "code": m["code"],
                "name": m["name"],
                "country": "United Arab Emirates",
                "emirate": m["emirate"],
                "all_branches": m["all_branches"],
                "branches": m["branch_keys"],
                "plan_key": m["plan"]["name"] if m["plan"] else "",
                "valid_from": m["valid_from"].strftime("%d %b %Y"),
                "valid_to": m["valid_to"].strftime("%d %b %Y"),
                "priority": str(m["priority"]),
            }
        context.update(
            {
                "incentive_branch_mappings": mappings,
                "mapping_counts": data.incentive_mapping_counts(mappings, all_branch_names),
                "incentive_plans_for_combo": [{"name": p["name"], "code": p["code"]} for p in plans],
                "branch_emirate_map": {b["name"]: b["location"] for b in branches_list},
            }
        )
        return context


class TargetView(HrmsScreenView):
    """RMS WEB APK UI.xlsx feedback -- built from the client's target.html
    mockup, not an FSD screen. Branch mapping is read-only here (a preview
    of Target Branch Mapping's own data), matching the mockup's own
    "coming in the next update" language for this screen."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = data.target_profiles()
        mappings = data.target_branch_mappings()
        branches_list = context["branches_list"]
        all_branch_names = [b["name"] for b in branches_list]
        branch_by_name = {b["name"]: b for b in branches_list}
        mapped_by_profile = {}
        for m in mappings:
            mapped_by_profile.setdefault(m["profile_code"], []).extend(data.mapping_branch_keys(m, all_branch_names))
        for i, p in enumerate(profiles):
            p["json_id"] = f"scr-record-target-{i}"
            p["mapped_json_id"] = f"scr-record-target-{i}-mapped"
            p["mapped_branches"] = sorted(set(mapped_by_profile.get(p["code"], [])))
            p["mapped_branch_objects"] = [
                {"name": n, "location": branch_by_name[n]["location"]}
                for n in p["mapped_branches"] if n in branch_by_name
            ]
            fields = {
                "code": p["code"],
                "name": p["name"],
                "type": p["type"],
                "collection_target": p["collection_target"],
                "customer_target": p["customer_target"],
                "year": p["period"].get("year", ""),
            }
            if p["type"] == "Monthly":
                fields["months"] = p["period"]["months"]
            elif p["type"] == "Daily":
                fields["month"] = p["period"]["month"]
                fields["day"] = p["period"]["day"]
            elif p["type"] == "Custom Date Range":
                fields["from_date"] = p["period"]["from_date"].strftime("%d %b %Y")
                fields["to_date"] = p["period"]["to_date"].strftime("%d %b %Y")
            p["fields_json"] = fields
        context.update(
            {
                "target_profiles": profiles,
                "target_counts": data.target_counts(profiles, mapped_by_profile.keys()),
            }
        )
        return context


class TargetBranchMappingView(HrmsScreenView):
    """RMS WEB APK UI.xlsx feedback -- built from the client's
    target-branch-mapping.html mockup, not an FSD screen."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branches_list = context["branches_list"]
        all_branch_names = [b["name"] for b in branches_list]
        branch_by_name = {b["name"]: b for b in branches_list}
        profiles = data.target_profiles()
        mappings = data.target_branch_mappings()
        for i, m in enumerate(mappings):
            m["json_id"] = f"scr-record-tbm-{i}"
            m["branches_json_id"] = f"scr-record-tbm-{i}-branches"
            m["branch_names"] = data.mapping_branch_keys(m, all_branch_names)
            m["branch_objects"] = [
                {"name": n, "location": branch_by_name[n]["location"]}
                for n in m["branch_names"] if n in branch_by_name
            ]
            m["profile"] = data.target_profile_by_code(m["profile_code"])
            m["expiring"] = data.is_expiring_soon(m["valid_to"])
            m["fields_json"] = {
                "code": m["code"],
                "name": m["name"],
                "country": "United Arab Emirates",
                "emirate": m["emirate"],
                "all_branches": m["all_branches"],
                "branches": m["branch_keys"],
                "profile_key": m["profile"]["name"] if m["profile"] else "",
                "valid_from": m["valid_from"].strftime("%d %b %Y"),
                "valid_to": m["valid_to"].strftime("%d %b %Y"),
                "priority": str(m["priority"]),
            }
        context.update(
            {
                "target_branch_mappings": mappings,
                "target_mapping_counts": data.target_mapping_counts(mappings, all_branch_names),
                "target_profiles_for_combo": [{"name": p["name"], "code": p["code"]} for p in profiles],
                "branch_emirate_map": {b["name"]: b["location"] for b in branches_list},
            }
        )
        return context


class DutyRosterView(HrmsScreenView):
    pass


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
