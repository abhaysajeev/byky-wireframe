from django.urls import path

from . import views

urlpatterns = [
    path(
        "integration/global-master-data-synchronization-replication/",
        views.Screen16_1.as_view(
            screen_no="16.1",
            screen_title="Global Master Data Synchronization & Replication",
            module_label="Integration",
            legacy_page="MasterDataSync.aspx",
            tier="A",
            phase=12,
            purpose="To orchestrate real-time and batch master data replication across distributed station branch databases, central OLTP databases, and mobile API caching nodes.",
            layout="Sync Engine Control Panel (Source Node, Target Node, Data Domain [Customer / Vehicle / Fare / RFID], Sync Mode [Real-Time CDC / Batch], Re-Sync Conflict Rule [Master Wins / Target Wins]), Active Replication Pipelines DataGrid.",
        ),
        name="integration-global-master-data-synchronization-replication",
    ),
    path(
        "integration/data-warehouse-schema-analytical-datamarts/",
        views.Screen16_2.as_view(
            screen_no="16.2",
            screen_title="Data Warehouse Schema & Analytical Datamarts",
            module_label="Integration",
            legacy_page="EnterpriseDataWarehouse.aspx",
            tier="C",
            phase=12,
            purpose="To manage the Star-Schema Enterprise Data Warehouse (EDW), inspect Fact and Dimension tables (`FactRentalTransactions`, `DimCustomer`, `DimVehicle`, `DimBranch`, `DimDate`), rebuild OLAP cubes, and execute BI Datamart refreshes.",
            layout="EDW Schema Directory Panel (Fact Tables, Dimension Tables, Aggregate Datamarts), Cube Processing Controls (Full Process / Incremental Process), Schema Refresh Audit DataGrid.",
        ),
        name="integration-data-warehouse-schema-analytical-datamarts",
    ),
    path(
        "integration/third-party-enterprise-api-connectors/",
        views.Screen16_3.as_view(
            screen_no="16.3",
            screen_title="Third-Party Enterprise API Connectors",
            module_label="Integration",
            legacy_page="ThirdPartyConnectorRegistry.aspx",
            tier="A",
            phase=12,
            purpose="To configure enterprise connectors to external accounting systems (SAP S/4HANA, Oracle Financials, Microsoft Dynamics 365), RTA Traffic Fine APIs, and Bank General Ledger sync engines.",
            layout="Enterprise Connector Registration Form (Connector Name, Enterprise System [SAP / Oracle / Dynamics / RTA], Endpoint Base URL, Client Credentials, Auth Type [OAuth2 / SAML / Mutual TLS], Active Status), Active Connectors DataGrid.",
        ),
        name="integration-third-party-enterprise-api-connectors",
    ),
    path(
        "integration/global-system-health-performance-dashboard/",
        views.Screen16_4.as_view(
            screen_no="16.4",
            screen_title="Global System Health & Performance Dashboard",
            module_label="Integration",
            legacy_page="SystemHealthMonitor.aspx",
            tier="C",
            phase=12,
            purpose="To display real-time system performance metrics, CPU / RAM utilization %, SQL Database IOPS, active SignalR WebSocket connections, API latency response averages (ms), and overall health across all 16 ERP modules.",
            layout="System KPI Metric Cards (Overall System Health 100%, Active User Sessions, DB Response Time ms, API Latency ms), Real-Time Server Performance Gauges, 16 Module Status Grid.",
        ),
        name="integration-global-system-health-performance-dashboard",
    ),
    path(
        "integration/final-integration-security-privilege-management/",
        views.IntegrationPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="16.5",
            screen_title="Final Integration Security Privilege Management",
            module_label="Integration",
            legacy_page="FinalIntegrationPrivilege.aspx",
            tier="D",
            phase=12,
            purpose="To configure fine-grained role-based security permissions specifically for master data replication, OLAP cube processing, third-party ERP connector editing, and global health monitoring.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per Integration Screen, Save/Reset Action Toolbar.",
        ),
        name="integration-final-integration-security-privilege-management",
    ),
]
