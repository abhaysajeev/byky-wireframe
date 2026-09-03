from django.urls import path

from . import views

urlpatterns = [
    path(
        "sfa/sales-lead-opportunity-management/",
        views.Screen7_1.as_view(
            screen_no="7.1",
            screen_title="Sales Lead & Opportunity Management",
            module_label="Sales Force",
            legacy_page="LeadManagement.aspx",
            tier="A",
            phase=8,
            purpose="To register corporate leads, track sales opportunity stages (New Lead, Qualified, Proposal Sent, Negotiation, Closed Won, Closed Lost), assign sales reps, and record client interaction logs.",
            layout="Form Panel (Company Name, Contact Person, Designation, Mobile No, Email, Lead Source, Estimated Deal Value AED, Expected Fleet Count, Sales Stage), Active Leads DataGrid with Pipeline Stage Badges.",
        ),
        name="sfa-sales-lead-opportunity-management",
    ),
    path(
        "sfa/corporate-b2b-rental-contract-setup/",
        views.Screen7_2.as_view(
            screen_no="7.2",
            screen_title="Corporate B2B Rental Contract Setup",
            module_label="Sales Force",
            legacy_page="CorporateContract.aspx",
            tier="A",
            phase=8,
            purpose="To draft, negotiate, approve, and execute long-term B2B corporate fleet leasing agreements, billing payment schedules, maintenance SLAs, and corporate discount structures.",
            layout="Header Contract Details Form (Contract No, Client Company, Start Date, End Date, Leased Vehicle Qty, Monthly Billing Amount AED, Payment Terms, Security Deposit), Executed Contracts DataGrid.",
        ),
        name="sfa-corporate-b2b-rental-contract-setup",
    ),
    path(
        "sfa/commercial-quotation-proposal-generator/",
        views.Screen7_3.as_view(
            screen_no="7.3",
            screen_title="Commercial Quotation & Proposal Generator",
            module_label="Sales Force",
            legacy_page="QuotationGenerator.aspx",
            tier="A",
            phase=8,
            purpose="To compose, calculate, generate, and email formal commercial rental price proposals and B2B fleet leasing quotations with itemized vehicle line items and discount structures.",
            layout="Quotation Header Form (Quote No, Client Lead Name, Valid Until Date, Discount Rate %, Currency), Line Item DataGrid (Vehicle Category, Qty, Rental Duration, Unit Rate AED, Subtotal), Generated Quotations Summary Grid.",
        ),
        name="sfa-commercial-quotation-proposal-generator",
    ),
    path(
        "sfa/sales-agent-commission-incentive-setup/",
        views.Screen7_4.as_view(
            screen_no="7.4",
            screen_title="Sales Agent Commission & Incentive Setup",
            module_label="Sales Force",
            legacy_page="SalesAgentCommission.aspx",
            tier="A",
            phase=8,
            purpose="To configure commission percentage structures, tiered sales incentives, monthly deal volume bonuses, and calculate monthly sales agent payouts.",
            layout="Form Panel (Sales Agent Employee, Target Monthly Sales AED, Base Commission %, Tier 2 Bonus %, Minimum Threshold AED), Agent Payout DataGrid.",
        ),
        name="sfa-sales-agent-commission-incentive-setup",
    ),
    path(
        "sfa/sales-pipeline-target-tracking/",
        views.Screen7_5.as_view(
            screen_no="7.5",
            screen_title="Sales Pipeline & Target Tracking",
            module_label="Sales Force",
            legacy_page="SalesTargetPipeline.aspx",
            tier="A",
            phase=8,
            purpose="To display real-time sales pipeline Kanban stages, quota achievement progress bars, monthly target vs actual variance analysis, and win-rate percentages.",
            layout="Top Sales Metric Cards (Total Pipeline Value AED, Monthly Quota AED, Target Achievement %, Active Opportunities Count), Sales Pipeline Kanban Board Widget, Sales Rep Performance DataGrid.",
        ),
        name="sfa-sales-pipeline-target-tracking",
    ),
    path(
        "sfa/sfa-security-privilege-management/",
        views.SfaPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="7.6",
            screen_title="SFA Security Privilege Management",
            module_label="Sales Force",
            legacy_page="SFAPrivilege.aspx",
            tier="D",
            phase=8,
            purpose="To configure fine-grained role-based security permissions specifically for corporate lead management, contract execution, commercial quotations, and sales commission approvals.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per SFA Screen, Save/Reset Action Toolbar.",
        ),
        name="sfa-sfa-security-privilege-management",
    ),
]
