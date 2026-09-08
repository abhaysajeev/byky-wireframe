from django.urls import path

from . import views

urlpatterns = [
    path(
        "sysadmin/global-erp-user-account-management/",
        views.Screen13_1.as_view(
            screen_no="13.1",
            screen_title="Global ERP User Account Management",
            module_label="System Administration",
            legacy_page="UserManagement.aspx",
            tier="A",
            phase=11,
            purpose="To provision enterprise user accounts, assign security roles, enforce 90-day password expiration rules, lock/unlock accounts after failed login attempts, and bind users to specific station branches.",
            layout="Form Panel (Username, Password, Confirm Password, Associated Employee, Assigned Role, Branch Station, Account Status [Active/Locked], Force Password Change Checkbox), Registered Users DataGrid.",
        ),
        name="sysadmin-global-erp-user-account-management",
    ),
    path(
        "sysadmin/system-role-authority-hierarchy/",
        views.Screen13_2.as_view(
            screen_no="13.2",
            screen_title="System Role & Authority Hierarchy",
            module_label="System Administration",
            legacy_page="RoleManagement.aspx",
            tier="A",
            phase=11,
            purpose="To define system access roles (SuperAdmin, StationManager, FleetManager, CustomerService, FinanceDirector), set authority level ranks, and configure role hierarchy descriptions.",
            layout="Form Panel (Role Code, Role Name, Authority Rank Level [1-10], Description, Active Status Checkbox), Active System Roles DataGrid.",
        ),
        name="sysadmin-system-role-authority-hierarchy",
    ),
    path(
        "sysadmin/global-application-configuration-settings/",
        views.GlobalConfigView.as_view(
            template_name="sysadmin_global_application_configuration_settings.html",
            screen_no="13.3",
            screen_title="Global Application Configuration & Settings",
            module_label="System Administration",
            legacy_page="SystemSettings.aspx",
            tier="A",
            phase=11,
            purpose="To configure enterprise-wide global parameters, company brand logo, default currency (AED), VAT percentage (5.00%), session timeout minutes (20 Mins), and system maintenance mode toggles.",
            layout="Company Branding Section (Company Legal Name, Logo Image Upload, Tax Registration TRN), Financial Settings (Default Currency, VAT Rate %, Security Deposit Default AED), Security Settings (Session Timeout Mins, Max Password Age Days), Save Global Settings Button.",
        ),
        name="sysadmin-global-application-configuration-settings",
    ),
    path(
        "sysadmin/enterprise-audit-log-compliance-viewer/",
        views.Screen13_4.as_view(
            screen_no="13.4",
            screen_title="Enterprise Audit Log & Compliance Viewer",
            module_label="System Administration",
            legacy_page="GlobalAuditLog.aspx",
            tier="C",
            phase=11,
            purpose="To inspect immutable enterprise audit trails, track user actions (CREATE, UPDATE, DELETE, LOGIN, EXPORT), review IP addresses, and export audit compliance logs.",
            layout="Filter Bar (User, Module, Action Type, Target DB Table, Date Range), Audit Trajectory DataGrid, Detailed Audit Change Inspector Modal.",
        ),
        name="sysadmin-enterprise-audit-log-compliance-viewer",
    ),
    path(
        "sysadmin/system-administration-privilege-management/",
        views.SysadminPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="13.5",
            screen_title="System Administration Privilege Management",
            module_label="System Administration",
            legacy_page="SystemAdminPrivilege.aspx",
            tier="D",
            phase=11,
            purpose="To configure security permissions specifically for provisioning user accounts, defining roles, modifying global application settings, and viewing audit logs.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per Admin Screen, Save/Reset Action Toolbar.",
        ),
        name="sysadmin-system-administration-privilege-management",
    ),
]
