"""Drawer specs for Module IMS screens.

Extracted from the screens' own markup when they moved to the shared byky
drawer, so the FSD field lists are exactly what they were -- see
apps/byky_core/drawers.py for the spec shape and how `options_from` resolves.
"""


ASSET = {
    "drawer_id": "drawerAsset",
    "scr_name": "asset",
    "add_label": "Add Asset",
    "title_field": "name",
    "sections": [
        {
            "title": "Identification",
            "fields": [
                {
                    "id": "code",
                    "label": "Asset Tag",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "name",
                    "label": "Asset Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "asset_class",
                    "label": "Asset Class",
                    "kind": "select",
                    "required": True,
                    "options_from": "asset_classes"
                },
                {
                    "id": "type",
                    "label": "Equipment Type",
                    "kind": "select",
                    "required": True,
                    "options_from": "asset_types",
                    "option_key": "name"
                },
                {
                    "id": "material_type",
                    "label": "Material Type",
                    "kind": "select",
                    "required": False,
                    "options": [
                        "Electrical",
                        "Electronics",
                        "Wooden",
                        "Metal",
                        "Plastic",
                        "Others"
                    ]
                },
                {
                    "id": "model",
                    "label": "Manufacturer / Model",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "serial",
                    "label": "Serial Number",
                    "kind": "text",
                    "required": False
                }
            ]
        },
        {
            "title": "Deployment",
            "fields": [
                {
                    "id": "station",
                    "label": "Posted To (Station)",
                    "kind": "select",
                    "required": False,
                    "options_from": "branches_list",
                    "option_key": "name"
                },
                {
                    "id": "custodian",
                    "label": "Custodian",
                    "kind": "select",
                    "required": False,
                    "options_from": "employees_list",
                    "option_key": "name"
                },
                {
                    "id": "ip",
                    "label": "IP Address",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "mac",
                    "label": "MAC Address",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "imei",
                    "label": "IMEI",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "msisdn",
                    "label": "SIM MSISDN",
                    "kind": "text",
                    "required": False
                }
            ]
        },
        {
            "title": "Lifecycle",
            "fields": [
                {
                    "id": "acquired",
                    "label": "Acquisition Date",
                    "kind": "date",
                    "required": False
                },
                {
                    "id": "cost",
                    "label": "Purchase Cost (AED)",
                    "kind": "number",
                    "required": False
                },
                {
                    "id": "supplier",
                    "label": "Supplier",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "warranty_from",
                    "label": "Warranty Period From",
                    "kind": "date",
                    "required": False,
                    "help": "Optional."
                },
                {
                    "id": "warranty_to",
                    "label": "Warranty Period To",
                    "kind": "date",
                    "required": False,
                    "help": "Optional."
                },
                {
                    "id": "condition",
                    "label": "Condition",
                    "kind": "select",
                    "required": False,
                    "options_from": "asset_conditions"
                },
                {
                    "id": "notes",
                    "label": "Notes",
                    "kind": "textarea",
                    "required": False
                }
            ]
        }
    ]
}

ASSETTYPE = {
    "drawer_id": "drawerAssettype",
    "scr_name": "assettype",
    "add_label": "Add Asset Type",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Type Code",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "name",
                    "label": "Equipment Type",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "asset_class",
                    "label": "Asset Class",
                    "kind": "select",
                    "required": True,
                    "options_from": "asset_classes"
                },
                {
                    "id": "identifier",
                    "label": "Tracked By",
                    "kind": "text",
                    "required": False,
                    "help": "The identifier a unit of this type is looked up by — an asset tag, an IMEI, an IP address."
                },
                {
                    "id": "location",
                    "label": "Typically Deployed",
                    "kind": "text",
                    "required": False
                }
            ]
        }
    ]
}

BRAND = {
    "drawer_id": "drawerBrand",
    "scr_name": "brand",
    "add_label": "Add Brand",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Brand Code",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "name",
                    "label": "Brand Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "website",
                    "label": "Website",
                    "kind": "text",
                    "required": False,
                    "placeholder": "https://"
                },
                {
                    "id": "",
                    "label": "Logo",
                    "kind": "file",
                    "required": False
                }
            ]
        }
    ]
}

CATEGORY = {
    "drawer_id": "drawerCategory",
    "scr_name": "category",
    "add_label": "Add Category",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Category Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "BYKY",
                    "lock_on_edit": True
                },
                {
                    "id": "name",
                    "label": "Category Name",
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
                    "id": "",
                    "label": "Icon Image",
                    "kind": "file",
                    "required": False
                }
            ]
        }
    ]
}

ITEM = {
    "drawer_id": "drawerItem",
    "scr_name": "item",
    "add_label": "Add Vehicle",
    "title_field": "name",
    "sections": [
        {
            "title": "Identification",
            "fields": [
                {
                    "id": "code",
                    "label": "Item Code",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "name",
                    "label": "Item Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "serial",
                    "label": "Barcode",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "rfid",
                    "label": "RFID Tag EPC",
                    "kind": "text",
                    "required": False,
                    "placeholder": "Enter RFID tag EPC"
                },
                {
                    "id": "",
                    "label": "Image",
                    "kind": "file",
                    "required": False
                }
            ]
        },
        {
            "title": "Classification",
            "fields": [
                {
                    "id": "brand",
                    "label": "Brand",
                    "kind": "select",
                    "required": False
                },
                {
                    "id": "category",
                    "label": "Category",
                    "kind": "select",
                    "required": True,
                    "options_from": "categories_list",
                    "option_key": "name"
                },
                {
                    "id": "subcategory",
                    "label": "Vehicle Type",
                    "kind": "select",
                    "required": False,
                    "options_from": "subcategories_list",
                    "option_key": "name"
                },
                {
                    "id": "unit",
                    "label": "Unit",
                    "kind": "select",
                    "required": False
                }
            ]
        },
        {
            "title": "Stock & Pricing",
            "note": "Data populated from ERP.",
            "fields": [
                {
                    "id": "reorder_level",
                    "label": "Reorder Level",
                    "kind": "number",
                    "required": False,
                    "readonly": True
                },
                {
                    "id": "min_qty",
                    "label": "Minimum Qty",
                    "kind": "number",
                    "required": False,
                    "readonly": True
                },
                {
                    "id": "cost_price",
                    "label": "Cost Price",
                    "kind": "number",
                    "required": False,
                    "readonly": True
                },
                {
                    "id": "rate",
                    "label": "Rental Rate / hour",
                    "kind": "number",
                    "required": False,
                    "readonly": True
                }
            ]
        }
    ]
}

PROMO = {
    "drawer_id": "drawerPromo",
    "scr_name": "promo",
    "add_label": "Add Promo Code",
    "title_field": "code",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Promo Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "SUMMER25"
                },
                {
                    "id": "promoDiscountType",
                    "label": "Discount Type",
                    "kind": "radio",
                    "required": True,
                    "options": [
                        "Percentage",
                        "Fixed Amount"
                    ],
                    "checked_option": "Percentage"
                },
                {
                    "id": "value",
                    "label": "Discount Value",
                    "kind": "number",
                    "required": True,
                    "placeholder": "0.00"
                },
                {
                    "id": "minSpend",
                    "label": "Minimum Spend (AED)",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00"
                },
                {
                    "id": "usageCap",
                    "label": "Usage Cap",
                    "kind": "number",
                    "required": False,
                    "placeholder": "e.g. 500"
                },
                {
                    "id": "perUserLimit",
                    "label": "Per-User Limit",
                    "kind": "number",
                    "required": False,
                    "placeholder": "e.g. 1"
                },
                {
                    "id": "validFrom",
                    "label": "Valid From",
                    "kind": "date",
                    "required": False,
                    "placeholder": "Select date"
                },
                {
                    "id": "validTo",
                    "label": "Valid To",
                    "kind": "date",
                    "required": False,
                    "placeholder": "Select date"
                }
            ]
        }
    ]
}

PUSH = {
    "drawer_id": "drawerPush",
    "scr_name": "push",
    "add_label": "New Push",
    "title_field": "title",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "title",
                    "label": "Notification Title",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "body",
                    "label": "Message Body",
                    "kind": "textarea",
                    "required": False
                },
                {
                    "id": "pushPlatform",
                    "label": "Platform",
                    "kind": "radio",
                    "required": False,
                    "options": [
                        "Android (FCM)",
                        "iOS (APNs)",
                        "Both"
                    ],
                    "checked_option": "Android (FCM)"
                },
                {
                    "id": "deepLink",
                    "label": "Deep Link Target",
                    "kind": "select",
                    "required": False
                },
                {
                    "id": "dispatchDate",
                    "label": "Dispatch Date",
                    "kind": "date",
                    "required": False,
                    "placeholder": "Select date"
                }
            ]
        }
    ]
}

REDEEM = {
    "drawer_id": "drawerRedeem",
    "scr_name": "redeem",
    "add_label": "Add Profile",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Redemption Code",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "name",
                    "label": "Profile Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "points",
                    "label": "Points Required",
                    "kind": "number",
                    "required": False,
                    "placeholder": "100"
                },
                {
                    "id": "cashValue",
                    "label": "AED Cash Value",
                    "kind": "number",
                    "required": False,
                    "placeholder": "10.00"
                },
                {
                    "id": "minBalance",
                    "label": "Min Redemption Balance",
                    "kind": "number",
                    "required": False,
                    "placeholder": "100"
                }
            ]
        }
    ]
}

STATUS = {
    "drawer_id": "drawerStatus",
    "scr_name": "status",
    "add_label": "Add Status",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Status Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "e.g. CNF"
                },
                {
                    "id": "name",
                    "label": "Status Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "e.g. Confirmed"
                },
                {
                    "id": "color",
                    "label": "Badge Colour",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "sequence",
                    "label": "Sequence Order",
                    "kind": "number",
                    "required": False,
                    "placeholder": "1"
                }
            ]
        }
    ]
}

SUBCATEGORY = {
    "drawer_id": "drawerSubcategory",
    "scr_name": "subcategory",
    "add_label": "Add Vehicle Type",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "parent",
                    "label": "Parent Category",
                    "kind": "select",
                    "required": True,
                    "options_from": "categories_list",
                    "option_key": "name"
                },
                {
                    "id": "code",
                    "label": "Vehicle Type Code",
                    "kind": "text",
                    "required": True,
                    "lock_on_edit": True
                },
                {
                    "id": "name",
                    "label": "Vehicle Type Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "description",
                    "label": "Description",
                    "kind": "textarea",
                    "required": False
                }
            ]
        }
    ]
}

TIER = {
    "drawer_id": "drawerTier",
    "scr_name": "tier",
    "add_label": "Add Tier",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Tier Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "e.g. GOLD"
                },
                {
                    "id": "name",
                    "label": "Tier Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "rate",
                    "label": "Points Earn Rate",
                    "kind": "number",
                    "required": False,
                    "placeholder": "1.00"
                },
                {
                    "id": "minSpend",
                    "label": "Min Spend Threshold (AED)",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00"
                }
            ]
        }
    ]
}

TRANSFER = {
    "drawer_id": "drawerTransfer",
    "scr_name": "transfer",
    "add_label": "New Transfer",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "doc_no",
                    "label": "Transfer Doc No",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "from_branch",
                    "label": "From Branch",
                    "kind": "select",
                    "required": True,
                    "options_from": "branches_list",
                    "option_key": "name"
                },
                {
                    "id": "to_branch",
                    "label": "To Branch",
                    "kind": "select",
                    "required": True,
                    "options_from": "branches_list",
                    "option_key": "name"
                },
                {
                    "id": "event_location",
                    "label": "Event Location",
                    "kind": "select",
                    "required": False,
                    "options_from": "event_locations_list",
                    "help": "Only for a transfer going to or from an event, not a branch."
                },
                {
                    "id": "dispatch_date",
                    "label": "Dispatch Date",
                    "kind": "date",
                    "required": False
                },
                {
                    "id": "driver",
                    "label": "Driver Name",
                    "kind": "text",
                    "required": False
                },
                {
                    "id": "items_count",
                    "label": "Items Count",
                    "kind": "number",
                    "required": False
                },
                {
                    "id": "remarks",
                    "label": "Remarks",
                    "kind": "textarea",
                    "required": False,
                    "width": 12
                }
            ]
        }
    ]
}

UNIT = {
    "drawer_id": "drawerUnit",
    "scr_name": "unit",
    "add_label": "Add Unit",
    "title_field": "name",
    "sections": [
        {
            "title": "",
            "fields": [
                {
                    "id": "code",
                    "label": "Unit Code",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "name",
                    "label": "Unit Name",
                    "kind": "text",
                    "required": True
                },
                {
                    "id": "description",
                    "label": "Description",
                    "kind": "textarea",
                    "required": False
                }
            ]
        }
    ]
}


# template variable -> spec, for the view to resolve in one call
SPECS = {

    "drawer_asset": ASSET,

    "drawer_assettype": ASSETTYPE,

    "drawer_brand": BRAND,

    "drawer_category": CATEGORY,

    "drawer_item": ITEM,

    "drawer_promo": PROMO,

    "drawer_push": PUSH,

    "drawer_redeem": REDEEM,

    "drawer_status": STATUS,

    "drawer_subcategory": SUBCATEGORY,

    "drawer_tier": TIER,

    "drawer_transfer": TRANSFER,

    "drawer_unit": UNIT,

}
