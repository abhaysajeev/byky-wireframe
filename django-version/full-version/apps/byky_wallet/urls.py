from django.urls import path

from . import views

urlpatterns = [
    path(
        "wallet/wallet-refund-request-approval-management/",
        views.Screen11_1.as_view(
            screen_no="11.1",
            screen_title="Wallet Refund Request & Approval Management",
            module_label="Wallet & Payments",
            legacy_page="WalletRefundRequest.aspx",
            tier="A",
            phase=10,
            purpose="To review, audit, approve, or reject customer wallet refund requests, verify IBAN bank details for payout, process security deposit returns, and record finance approval audit logs.",
            layout="Refund Claim Details Panel (Claim ID, Customer Name, Mobile No, Wallet Balance AED, Claimed Refund Amount AED, Refund Reason, IBAN Number, Bank Name), Approver Action Controls (Approve & Dispatch Payout, Reject Claim), Refund Requests DataGrid.",
        ),
        name="wallet-wallet-refund-request-approval-management",
    ),
    path(
        "wallet/payment-gateway-provider-webhook-integration/",
        views.Screen11_2.as_view(
            screen_no="11.2",
            screen_title="Payment Gateway Provider & Webhook Integration",
            module_label="Wallet & Payments",
            legacy_page="PaymentGatewaySetup.aspx",
            tier="A",
            phase=10,
            purpose="To configure online payment gateway credentials (Network International, Stripe, Apple Pay, PayCaps), Merchant IDs, Webhook URL endpoints, API Secret Tokens, and test transaction processing.",
            layout="Form Panel (Gateway Provider Name, Merchant ID, API Key, Webhook Secret Token, Currency [AED], Environment [Sandbox/Production], Active Gateway Checkbox), Configured Payment Gateways DataGrid.",
        ),
        name="wallet-payment-gateway-provider-webhook-integration",
    ),
    path(
        "wallet/security-deposit-hold-refund-reconciliation/",
        views.Screen11_3.as_view(
            screen_no="11.3",
            screen_title="Security Deposit Hold & Refund Reconciliation",
            module_label="Wallet & Payments",
            legacy_page="SecurityDepositReconciliation.aspx",
            tier="A",
            phase=10,
            purpose="To reconcile pre-authorized credit card security deposit holds (AED 300 / AED 500), release pre-auth holds upon vehicle return inspection, or capture deposit funds for vehicle damages.",
            layout="Deposit Reconciliation Search Header (Agreement No, Customer Name, Deposit Status [Held / Released / Captured / Pending Audit]), Reconciliation Audit Panel, Deposit Pre-Auth Holds DataGrid.",
        ),
        name="wallet-security-deposit-hold-refund-reconciliation",
    ),
    path(
        "wallet/customer-wallet-ledger-transaction-audit/",
        views.Screen11_4.as_view(
            screen_no="11.4",
            screen_title="Customer Wallet Ledger & Transaction Audit",
            module_label="Wallet & Payments",
            legacy_page="CustomerWalletLedger.aspx",
            tier="A",
            phase=10,
            purpose="To inspect, audit, adjust, or manually credit/debit customer wallet balances, search transaction logs, and generate financial wallet reconciliation statements.",
            layout="Customer Search Header, Wallet Balance Summary Card, Manual Adjustment Panel (Adjustment Type [Credit / Debit], Amount AED, Reason, Reference No), Transaction Audit DataGrid.",
        ),
        name="wallet-customer-wallet-ledger-transaction-audit",
    ),
    path(
        "wallet/wallet-security-privilege-management/",
        views.WalletPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="11.5",
            screen_title="Wallet Security Privilege Management",
            module_label="Wallet & Payments",
            legacy_page="WalletPrivilege.aspx",
            tier="D",
            phase=10,
            purpose="To configure fine-grained role-based security permissions specifically for refund approvals, payment gateway setup, deposit hold releases, and manual wallet adjustments.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per Wallet Screen, Save/Reset Action Toolbar.",
        ),
        name="wallet-wallet-security-privilege-management",
    ),
]
