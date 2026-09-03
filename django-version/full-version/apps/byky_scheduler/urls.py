from django.urls import path

from . import views

urlpatterns = [
    path(
        "scheduler/cron-job-background-scheduler-management/",
        views.Screen12_1.as_view(
            screen_no="12.1",
            screen_title="Cron Job & Background Scheduler Management",
            module_label="Scheduler",
            legacy_page="JobSchedulerManager.aspx",
            tier="A",
            phase=11,
            purpose="To configure automated background jobs, set 5-field cron expressions (e.g., `0 0 * * *`), trigger manual job executions, pause/resume worker threads, and inspect execution duration logs.",
            layout="Form Panel (Job Name, Job Class, Cron Expression, Execution Frequency, Max Retries, Active Status), Active Scheduler Jobs DataGrid with Live Execution Status Badges.",
        ),
        name="scheduler-cron-job-background-scheduler-management",
    ),
    path(
        "scheduler/etl-data-pipeline-database-sync/",
        views.Screen12_2.as_view(
            screen_no="12.2",
            screen_title="ETL Data Pipeline & Database Sync",
            module_label="Scheduler",
            legacy_page="DataPipelineSync.aspx",
            tier="A",
            phase=11,
            purpose="To configure bulk ETL data extraction pipelines, database replica synchronization, telemetry data aggregation, and data warehouse batch loading.",
            layout="Pipeline Configuration Panel (Pipeline Name, Source DB Connection, Target DB Warehouse, Batch Size [1000-10000 rows], Sync Interval Mins, Transformation Script), Configured Data Pipelines DataGrid.",
        ),
        name="scheduler-etl-data-pipeline-database-sync",
    ),
    path(
        "scheduler/automated-system-maintenance-log-purge/",
        views.Screen12_3.as_view(
            screen_no="12.3",
            screen_title="Automated System Maintenance & Log Purge",
            module_label="Scheduler",
            legacy_page="AuditLogCleanupJob.aspx",
            tier="A",
            phase=11,
            purpose="To schedule automated system database maintenance tasks, index defragmentation, temp table cleanup, and archive audit logs older than retention thresholds (e.g., 90 days).",
            layout="Maintenance Policy Setup Panel (Log Retention Days [30-365 Days], Target Tables [Audit Log / Telemetry Log / Temp Tables], Defragment Index Threshold %, Execution Time), Maintenance History DataGrid.",
        ),
        name="scheduler-automated-system-maintenance-log-purge",
    ),
    path(
        "scheduler/automated-notification-queue-dispatcher/",
        views.Screen12_4.as_view(
            screen_no="12.4",
            screen_title="Automated Notification Queue & Dispatcher",
            module_label="Scheduler",
            legacy_page="BatchNotificationJob.aspx",
            tier="C",
            phase=11,
            purpose="To monitor background notification queue worker threads, dispatch queued SMS/Email messages, process retry attempts for failed dispatches, and inspect queue throughput.",
            layout="Queue Dispatcher Metric Cards (Pending Queue Count, Dispatched Today, Failed Retry Queue, Dispatch Speed / Sec), Worker Thread Settings Form, Queued Notification Items DataGrid.",
        ),
        name="scheduler-automated-notification-queue-dispatcher",
    ),
    path(
        "scheduler/scheduler-security-privilege-management/",
        views.SchedulerPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="12.5",
            screen_title="Scheduler Security Privilege Management",
            module_label="Scheduler",
            legacy_page="SchedulerPrivilege.aspx",
            tier="D",
            phase=11,
            purpose="To configure fine-grained role-based security permissions specifically for triggering manual cron jobs, modifying ETL data pipelines, executing database purges, and managing worker threads.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per Scheduler Screen, Save/Reset Action Toolbar.",
        ),
        name="scheduler-scheduler-security-privilege-management",
    ),
]
