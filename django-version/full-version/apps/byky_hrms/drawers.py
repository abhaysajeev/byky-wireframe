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
                    "placeholder": "MECH",
                    "lock_on_edit": True
                },
                {
                    "id": "title",
                    "label": "Designation Title",
                    "kind": "text",
                    "required": True,
                    "placeholder": "Mechanic"
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
                    "placeholder": "BYKY001",
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
                    "required": False
                },
                {
                    "id": "marital_status",
                    "label": "Marital Status",
                    "kind": "select",
                    "required": False
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


# template variable -> spec, for the view to resolve in one call
SPECS = {

    "drawer_address": ADDRESS,

    "drawer_designation": DESIGNATION,

    "drawer_employee": EMPLOYEE,

    "drawer_grade": GRADE,

}
