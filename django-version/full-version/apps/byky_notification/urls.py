from django.urls import path

from . import views

urlpatterns = [
    path(
        "notification/notification-broadcasting-template-master/",
        views.Screen10_1.as_view(
            screen_no="10.1",
            screen_title="Notification Broadcasting & Template Master",
            module_label="Notifications",
            legacy_page="Notification.aspx",
            tier="A",
            phase=10,
            purpose="To compose, schedule, and broadcast push notifications to mobile app users, manage notification templates (Rental Expiry, Wallet Low Balance, Promo Offers), and view dispatch analytics.",
            layout="Notification Composition Form (Title, Target Audience [All App Users / Active Renters / VIP Customers], Channel [Mobile Push / SMS / Email], Message Body, Scheduled Time), Broadcast Log DataGrid.",
        ),
        name="notification-notification-broadcasting-template-master",
    ),
    path(
        "notification/system-security-alert-dispatch-monitoring/",
        views.Screen10_2.as_view(
            screen_no="10.2",
            screen_title="System Security Alert Dispatch & Monitoring",
            module_label="Notifications",
            legacy_page="AlertView.aspx",
            tier="C",
            phase=10,
            purpose="To monitor real-time automated system security alerts (Geofence Breach, Speeding Violation, Battery Depletion, RFID Siren Alarm, Low Hardware Storage) and manage dispatch rules.",
            layout="Alert Severity Filter Bar (Critical, Warning, Info), Real-Time Alert Monitor Stream, Alert Resolution Panel, Security Dispatch Audit DataGrid.",
        ),
        name="notification-system-security-alert-dispatch-monitoring",
    ),
    path(
        "notification/sms-gateway-provider-gateway-configuration/",
        views.Screen10_3.as_view(
            screen_no="10.3",
            screen_title="SMS Gateway Provider & Gateway Configuration",
            module_label="Notifications",
            legacy_page="SmsGatewaySetup.aspx",
            tier="A",
            phase=10,
            purpose="To configure cellular SMS gateway API endpoints (Twilio, Etisalat SMS API, Infobip), API Key credentials, Sender IDs, rate limits, and fallback gateway routing.",
            layout="Form Panel (Provider Name, Gateway API URL, API Key / Secret, Sender ID [BYKY-RENT], Max Daily Quota, Active Status), Configured SMS Gateways DataGrid.",
        ),
        name="notification-sms-gateway-provider-gateway-configuration",
    ),
    path(
        "notification/email-smtp-server-html-template-setup/",
        views.Screen10_4.as_view(
            screen_no="10.4",
            screen_title="Email SMTP Server & HTML Template Setup",
            module_label="Notifications",
            legacy_page="EmailTemplateSetup.aspx",
            tier="A",
            phase=10,
            purpose="To configure SMTP mail server credentials (Host, Port 587/465, SSL/TLS, Username, Password), From Email Address, and design rich HTML email templates (Invoices, Rental Confirmations, Password Resets).",
            layout="SMTP Server Configuration Form, WYSIWYG HTML Template Editor, Dynamic Parameter Tags List ({CustomerName}, {AgreementNo}, {RentalFee}), Test Email Dispatch Button, Active Email Templates Grid.",
        ),
        name="notification-email-smtp-server-html-template-setup",
    ),
    path(
        "notification/notification-security-privilege-management/",
        views.NotificationPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="10.5",
            screen_title="Notification Security Privilege Management",
            module_label="Notifications",
            legacy_page="NotificationPrivilege.aspx",
            tier="D",
            phase=10,
            purpose="To configure fine-grained role-based security permissions specifically for broadcasting push notifications, acknowledging security alerts, modifying SMS gateway credentials, and updating SMTP servers.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per Notification Screen, Save/Reset Action Toolbar.",
        ),
        name="notification-notification-security-privilege-management",
    ),
]
