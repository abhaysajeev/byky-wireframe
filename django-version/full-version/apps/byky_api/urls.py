from django.urls import path

from . import views

urlpatterns = [
    path(
        "api/mobile-rest-api-gateway-route-registry/",
        views.Screen14_1.as_view(
            screen_no="14.1",
            screen_title="Mobile REST API Gateway & Route Registry",
            module_label="Mobile API",
            legacy_page="MobileApiEndpoints.aspx",
            tier="A",
            phase=11,
            purpose="To register, version, monitor, and throttle RESTful API endpoints used by mobile apps (e.g. `/api/v1/vehicles/catalog`, `/api/v1/booking/checkout`, `/api/v1/lock/release`), and set rate-limiting policies.",
            layout="Form Panel (Endpoint Route Name, HTTP Verb [GET/POST/PUT/DELETE], Controller Route, Version [v1/v2], Rate Limit Req/Min, Requires Auth Checkbox), Active Registered API Routes DataGrid.",
        ),
        name="api-mobile-rest-api-gateway-route-registry",
    ),
    path(
        "api/jwt-security-token-oauth-authentication-service/",
        views.Screen14_2.as_view(
            screen_no="14.2",
            screen_title="JWT Security Token & OAuth Authentication Service",
            module_label="Mobile API",
            legacy_page="TokenAuthService.aspx",
            tier="A",
            phase=11,
            purpose="To configure JWT HMAC-SHA256 signing secret keys, token expiration lifetimes (e.g., Access Token 60 Mins, Refresh Token 30 Days), revoke active bearer tokens, and inspect active mobile app login sessions.",
            layout="JWT Secret Key Configuration Form, Refresh Token Policy Setup, Active Bearer Token Sessions DataGrid, Revoke Token Action Buttons.",
        ),
        name="api-jwt-security-token-oauth-authentication-service",
    ),
    path(
        "api/fcm-apns-mobile-push-dispatch-engine/",
        views.Screen14_3.as_view(
            screen_no="14.3",
            screen_title="FCM & APNS Mobile Push Dispatch Engine",
            module_label="Mobile API",
            legacy_page="PushNotificationDispatcher.aspx",
            tier="A",
            phase=11,
            purpose="To configure Firebase Cloud Messaging (FCM) Server Keys, Apple Push Notification service (APNs) Auth Key certificates, bundle IDs, and monitor push dispatch latency.",
            layout="Form Panel (Push Channel [FCM Android / APNs iOS], App Bundle ID, Server Key / Auth Certificate Upload, Key ID, Team ID), Push Dispatcher Status, Push Logs DataGrid.",
        ),
        name="api-fcm-apns-mobile-push-dispatch-engine",
    ),
    path(
        "api/third-party-api-webhook-partner-integration/",
        views.Screen14_4.as_view(
            screen_no="14.4",
            screen_title="Third-Party API Webhook & Partner Integration",
            module_label="Mobile API",
            legacy_page="ThirdPartyIntegrationBus.aspx",
            tier="A",
            phase=11,
            purpose="To configure external B2B partner integrations (Hotel Concierge portals, Tourism Board APIs, Payment Gateway Webhooks), HMAC secret signing, and inspect incoming/outgoing webhook payloads.",
            layout="Partner Integration Form (Partner Name, Webhook Callback URL, Secret Signing Key, Event Subscriptions [Booking Created / Trip Ended / Payment Settled], Active Checkbox), Registered Webhooks DataGrid.",
        ),
        name="api-third-party-api-webhook-partner-integration",
    ),
    path(
        "api/mobile-api-security-privilege-management/",
        views.ApiPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="14.5",
            screen_title="Mobile API Security Privilege Management",
            module_label="Mobile API",
            legacy_page="MobileApiPrivilege.aspx",
            tier="D",
            phase=11,
            purpose="To configure fine-grained security permissions specifically for managing mobile REST endpoints, revoking JWT bearer tokens, configuring FCM/APNs push keys, and editing third-party partner webhooks.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per API Screen, Save/Reset Action Toolbar.",
        ),
        name="api-mobile-api-security-privilege-management",
    ),
]
