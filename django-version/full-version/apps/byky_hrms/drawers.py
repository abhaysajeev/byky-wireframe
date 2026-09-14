"""Drawer specs for Module HRMS screens.

Extracted from the screens' own markup when they moved to the shared byky
drawer, so the FSD field lists are exactly what they were -- see
apps/byky_core/drawers.py for the spec shape and how `options_from` resolves.
"""


ADDRESS = {
    "drawer_id": "drawerAddress",
    "scr_name": "address",
    "add_label": "Add Address",
    "title_field": "employee",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "employee",
                    "label": "Employee",
                    "kind": "select",
                    "required": True,
                    "options_from": "employees_list",
                    "option_key": "name"
                },
                {
                    "id": "line1",
                    "label": "Address Line 1",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "line2",
                    "label": "Address Line 2",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "building",
                    "label": "Building Name",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "flat",
                    "label": "Flat / Room No",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "city",
                    "label": "City",
                    "kind": "text",
                    "required": False
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
                    "id": "zip",
                    "label": "Zip Code",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "landlord",
                    "label": "Landlord Name",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "landlord_phone",
                    "label": "Landlord Contact Phone",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "home_country_address",
                    "label": "Home Country Address",
                    "kind": "textarea",
                    "required": False,
                    "help": "The employee's permanent address in their home country."
                },
                {
                    "id": "home_contact_person",
                    "label": "Contact Person Name",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "home_contact_no",
                    "label": "Contact No",
                    "kind": "text",
                    "required": False
                }
            ]
        }
    ]
}

DESIGNATION = {
    "drawer_id": "drawerDesignation",
    "scr_name": "designation",
    "add_label": "Add Designation",
    "title_field": "title",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Designation Code",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "title",
                    "label": "Designation Title",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "description",
                    "label": "Description",
                    "kind": "textarea",
                    "required": False
                },
                {
                    "id": "rank",
                    "label": "Rank Order",
                    "kind": "number",
                    "required": False
                }
            ]
        }
    ]
}

EMPLOYEE = {
    "drawer_id": "drawerEmployee",
    "scr_name": "employee",
    "add_label": "Add Employee",
    "title_field": "name",
    "sections": [
        {
            "title": "Identity",
            "fields": [
                {
                    "id": "emp_no",
                    "label": "Employee Code",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "",
                    "label": "Photo",
                    "kind": "file",
                    "required": False
                },
                {
                    "id": "first_name",
                    "label": "First Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "middle_name",
                    "label": "Middle Name",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "last_name",
                    "label": "Last Name",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "designation",
                    "label": "Designation",
                    "kind": "select",
                    "required": True,
                    "options_from": "designations_list",
                    "option_key": "title"
                }
            ]
        },
        {
            "title": "Personal",
            "fields": [
                {
                    "id": "dob",
                    "label": "Date of Birth",
                    "kind": "date",
                    "required": False,
                    "placeholder": "Not captured"
                },
                {
                    "id": "gender",
                    "label": "Gender",
                    "kind": "select",
                    "required": False,
                    "options": [
                        "Male",
                        "Female",
                        "Other"
                    ]
                },
                {
                    "id": "marital_status",
                    "label": "Marital Status",
                    "kind": "select",
                    "required": False,
                    "options": [
                        "Single",
                        "Married",
                        "Widowed",
                        "Divorced"
                    ]
                },
                {
                    "id": "nationality",
                    "label": "Nationality",
                    "kind": "select",
                    "required": False,
                    "options_from": "nationalities_list"
                }
            ]
        },
        {
            "title": "Documents",
            "fields": [
                {
                    "id": "passport_no",
                    "label": "Passport Number",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Not captured"
                },
                {
                    "id": "passport_expiry",
                    "label": "Passport Expiry",
                    "kind": "date",
                    "required": False
                },
                {
                    "id": "visa_no",
                    "label": "Visa Number",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Not captured"
                },
                {
                    "id": "visa_expiry",
                    "label": "Visa Expiry",
                    "kind": "date",
                    "required": False
                },
                {
                    "id": "eid_no",
                    "label": "Emirates ID Number",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Not captured"
                },
                {
                    "id": "eid_expiry",
                    "label": "Emirates ID Expiry",
                    "kind": "date",
                    "required": False
                },
                {
                    "id": "labor_no",
                    "label": "Labour Card Number",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Not captured"
                },
                {
                    "id": "labor_expiry",
                    "label": "Labour Card Expiry",
                    "kind": "date",
                    "required": False
                },
                {
                    "id": "salary_bank",
                    "label": "Salary Bank",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Not captured"
                },
                {
                    "id": "salary_bank_account",
                    "label": "Salary Account Details",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Not captured"
                }
            ]
        },
        {
            "title": "Contact",
            "fields": [
                {
                    "id": "mobile",
                    "label": "Mobile Number",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Not captured"
                },
                {
                    "id": "email",
                    "label": "Email Address",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Not captured"
                },
                {
                    "id": "uae_address",
                    "label": "UAE Address",
                    "kind": "textarea",
                    "required": False,
                    "width": 12
                },
                {
                    "id": "home_country_address",
                    "label": "Home Country Address",
                    "kind": "textarea",
                    "required": False,
                    "width": 12
                },
                {
                    "id": "emergency_person",
                    "label": "Emergency Contact Person",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "emergency_phone",
                    "label": "Emergency Phone",
                    "kind": "text",
                    "required": False
                }
            ]
        }
    ]
}

GRADE = {
    "drawer_id": "drawerGrade",
    "scr_name": "grade",
    "add_label": "Add Grade",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Grade Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "G1"
                },
                {
                    "id": "name",
                    "label": "Grade Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "min_salary",
                    "label": "Min Salary",
                    "kind": "number",
                    "required": False
                },
                {
                    "id": "max_salary",
                    "label": "Max Salary",
                    "kind": "number",
                    "required": False
                }
            ]
        }
    ]
}


# RMS WEB APK UI.xlsx feedback -- "new html" client mockups, not FSD screens.
# See apps/byky_hrms/data.py's module note above INCENTIVE_PLAN's data
# functions for how the mockup's invented user-type list was reconciled
# against the real designation master.
INCENTIVE_PLAN = {
    "drawer_id": "drawerIncentivePlan",
    "scr_name": "incentive-plan",
    "add_label": "Add Incentive Plan",
    "title_field": "name",
    "size": "wide",
    "sections": [
        {
            "title": "Plan Details",
            "fields": [
                {"id": "code", "label": "Incentive Profile Code", "kind": "text", "required": True, "lock_on_edit": True, "readonly": True},
                {"id": "name", "label": "Incentive Profile Name", "kind": "text", "required": True},
            ],
        },
        {
            "title": "User Types",
            "note": "Cashier with RMS Login, Cashier without RMS Login, and Labour are listed first since most plans start there; every other designation from the HR module follows in headcount order.",
            "fields": [
                {
                    "id": "user_types",
                    "label": "User Type(s)",
                    "kind": "multiselect",
                    "required": True,
                    "options_from": "incentive_user_types_list",
                    "option_key": "title",
                    "placeholder": "Select user type(s)",
                },
            ],
        },
        {
            "title": "% of Collection & Dividend",
            "note": "If a branch achieves its target, employees who worked there that month are eligible for incentive, paid from the branch's total collection. Since staff can move between branches day to day (via Duty Roster), it's worked out on a daily pro-rated basis, with each row's dividend rule deciding how that day's share is divided.",
            "fields": [
                {"id": "breakdown", "label": "", "kind": "custom"},
            ],
        },
    ],
}


INCENTIVE_BRANCH_MAPPING = {
    "drawer_id": "drawerIncentiveBranchMapping",
    "scr_name": "incentive-branch-mapping",
    "add_label": "Add Mapping",
    "title_field": "name",
    "size": "wide",
    "sections": [
        {
            "title": "Mapping Details",
            "fields": [
                {"id": "code", "label": "Mapping Code", "kind": "text", "required": True, "lock_on_edit": True, "readonly": True},
                {"id": "name", "label": "Mapping Name", "kind": "text", "required": True, "placeholder": "Enter mapping name"},
            ],
        },
        {
            "title": "Branch Selection",
            "fields": [
                {"id": "country", "label": "Country", "kind": "select", "required": True, "options_from": "countries_list", "option_key": "name"},
                {"id": "emirate", "label": "Emirate", "kind": "select", "options_from": "states_list", "option_key": "name", "help": "All Emirates if left blank."},
                {"id": "all_branches", "label": "", "kind": "checkbox", "placeholder": "All Branches"},
                {
                    "id": "branches", "label": "Branches", "kind": "multiselect", "required": True,
                    "options_from": "branches_list", "option_key": "name", "placeholder": "Select branch(es)",
                    "show_if": "all_branches:no",
                },
            ],
        },
        {
            "title": "Incentive Plan & Validity",
            "fields": [
                {"id": "plan_key", "label": "Incentive Plan", "kind": "combo", "required": True, "combo_source": "incentive-plans-data", "combo_key": "name", "combo_sub": "code", "placeholder": "Search plan by code or name..."},
                {"id": "valid_from", "label": "Valid From", "kind": "date", "required": True},
                {"id": "valid_to", "label": "Valid To", "kind": "date", "required": True},
            ],
        },
        {
            "title": "Priority",
            "fields": [
                {
                    "id": "priority", "label": "Priority (1 – 10)", "kind": "select", "required": True,
                    "options": [str(n) for n in range(1, 11)], "default": "5",
                    "help": "1 = highest priority. If a branch has more than one active incentive mapping at the same time, the mapping with the lowest priority number is the one applied.",
                },
            ],
        },
    ],
}


TARGET_BRANCH_MAPPING = {
    "drawer_id": "drawerTargetBranchMapping",
    "scr_name": "target-branch-mapping",
    "add_label": "Add Mapping",
    "title_field": "name",
    "size": "wide",
    "sections": [
        {
            "title": "Mapping Details",
            "fields": [
                {"id": "code", "label": "Mapping Code", "kind": "text", "required": True, "lock_on_edit": True, "readonly": True},
                {"id": "name", "label": "Mapping Name", "kind": "text", "required": True, "placeholder": "Enter mapping name"},
            ],
        },
        {
            "title": "Branch Selection",
            "fields": [
                {"id": "country", "label": "Country", "kind": "select", "required": True, "options_from": "countries_list", "option_key": "name"},
                {"id": "emirate", "label": "Emirate", "kind": "select", "options_from": "states_list", "option_key": "name", "help": "All Emirates if left blank."},
                {"id": "all_branches", "label": "", "kind": "checkbox", "placeholder": "All Branches"},
                {
                    "id": "branches", "label": "Branches", "kind": "multiselect", "required": True,
                    "options_from": "branches_list", "option_key": "name", "placeholder": "Select branch(es)",
                    "show_if": "all_branches:no",
                },
            ],
        },
        {
            "title": "Target Profile & Validity",
            "fields": [
                {"id": "profile_key", "label": "Target Profile", "kind": "combo", "required": True, "combo_source": "target-profiles-data", "combo_key": "name", "combo_sub": "code", "placeholder": "Search profile by code or name..."},
                {"id": "valid_from", "label": "Valid From", "kind": "date", "required": True},
                {"id": "valid_to", "label": "Valid To", "kind": "date", "required": True},
            ],
        },
        {
            "title": "Priority",
            "fields": [
                {
                    "id": "priority", "label": "Priority (1 – 10)", "kind": "select", "required": True,
                    "options": [str(n) for n in range(1, 11)], "default": "5",
                    "help": "1 = highest priority. If a branch has more than one active target mapping at the same time, the mapping with the lowest priority number is the one applied.",
                },
            ],
        },
    ],
}


TARGET_PROFILE = {
    "drawer_id": "drawerTargetProfile",
    "scr_name": "target-profile",
    "add_label": "Add Target Profile",
    "title_field": "name",
    "size": "wide",
    "sections": [
        {
            "title": "Profile Type & Period",
            "fields": [
                {"id": "type", "label": "", "kind": "custom"},
                {"id": "year", "label": "Year", "kind": "select", "options": ["2025", "2026", "2027"], "default": "2026", "show_if": "type:Yearly|Monthly|Daily"},
                {"id": "months", "label": "Month(s)", "kind": "multiselect", "options": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], "placeholder": "Select month(s)", "show_if": "type:Monthly"},
                {"id": "month", "label": "Month", "kind": "select", "options": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], "show_if": "type:Daily"},
                {"id": "day", "label": "Day", "kind": "select", "options": [str(n) for n in range(1, 32)], "show_if": "type:Daily"},
                {"id": "from_date", "label": "From Date", "kind": "date", "show_if": "type:Custom Date Range"},
                {"id": "to_date", "label": "To Date", "kind": "date", "show_if": "type:Custom Date Range"},
            ],
        },
        {
            "title": "Profile Details",
            "fields": [
                {"id": "code", "label": "Target Profile Code", "kind": "text", "required": True, "placeholder": "e.g. TP-2026-001"},
                {"id": "name", "label": "Target Profile Name", "kind": "text", "required": True, "placeholder": "Enter target profile name"},
            ],
        },
        {
            "title": "Targets",
            "fields": [
                {"id": "collection_target", "label": "Total Collection Target (AED)", "kind": "number", "required": True, "placeholder": "Enter total collection target"},
                {"id": "customer_target", "label": "New Customer Target (count)", "kind": "number", "required": True, "placeholder": "Enter new customer target"},
            ],
        },
    ],
}


# template variable -> spec, for the view to resolve in one call
SPECS = {

    "drawer_address": ADDRESS,

    "drawer_designation": DESIGNATION,

    "drawer_employee": EMPLOYEE,

    "drawer_grade": GRADE,

    "drawer_incentive_plan": INCENTIVE_PLAN,

    "drawer_incentive_branch_mapping": INCENTIVE_BRANCH_MAPPING,

    "drawer_target_branch_mapping": TARGET_BRANCH_MAPPING,

    "drawer_target_profile": TARGET_PROFILE,

}
