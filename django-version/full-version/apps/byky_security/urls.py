from django.urls import path

from . import views

urlpatterns = [
    path(
        "security/aes-256-data-encryption-key-rotation-manager/",
        views.Screen15_1.as_view(
            screen_no="15.1",
            screen_title="AES-256 Data Encryption & Key Rotation Manager",
            module_label="System Security",
            legacy_page="DataEncryptionConfig.aspx",
            tier="A",
            phase=12,
            purpose="To manage AES-256 GCM master encryption keys, configure Transparent Data Encryption (TDE) for SQL databases, execute scheduled master key rotations (90 days), and re- encrypt sensitive customer PII fields.",
            layout="Form Panel (Master Key Alias, Algorithm [AES-256-GCM], Active Key Version, Key Rotation Days [30-180], Hardware Security Module [HSM] Binding, Re-encrypt Database Fields Checkbox), Encryption Key Version History DataGrid.",
        ),
        name="security-aes-256-data-encryption-key-rotation-manager",
    ),
    path(
        "security/session-security-2fa-ip-whitelist-governance/",
        views.Screen15_2.as_view(
            screen_no="15.2",
            screen_title="Session Security, 2FA & IP Whitelist Governance",
            module_label="System Security",
            legacy_page="SessionSecurityPolicy.aspx",
            tier="A",
            phase=12,
            purpose="To configure IP address whitelisting for admin portal access, enforce Two-Factor Authentication (2FA TOTP / SMS OTP), set maximum concurrent user login limits, and manage active session terminations.",
            layout="IP Whitelist Entry Form (Rule Name, IP Address / CIDR Range [192.168.1.0/24], Description, Access Level), 2FA Global Policy Toggles (Enforce 2FA for Admin Roles), Configured IP Whitelist Rules DataGrid.",
        ),
        name="security-session-security-2fa-ip-whitelist-governance",
    ),
    path(
        "security/database-backup-disaster-recovery-orchestrator/",
        views.Screen15_3.as_view(
            screen_no="15.3",
            screen_title="Database Backup & Disaster Recovery Orchestrator",
            module_label="System Security",
            legacy_page="DatabaseBackupDisasterRecovery.aspx",
            tier="A",
            phase=12,
            purpose="To configure automated database full/diff/log backup schedules, off-site cloud storage replication (Azure Blob / AWS S3), AES-256 backup file encryption, and execute point-in- time disaster recovery restores.",
            layout="Backup Configuration Panel (Backup Type [Full / Differential / Transaction Log], Schedule Cron, Retention Days, Off-Site Storage Provider, Encryption Password), Disaster Recovery Restore Panel, Executed Backups DataGrid.",
        ),
        name="security-database-backup-disaster-recovery-orchestrator",
    ),
    path(
        "security/pci-dss-gdpr-compliance-audit-manager/",
        views.Screen15_4.as_view(
            screen_no="15.4",
            screen_title="PCI-DSS & GDPR Compliance Audit Manager",
            module_label="System Security",
            legacy_page="PciDssComplianceAudit.aspx",
            tier="A",
            phase=12,
            purpose="To run automated PCI-DSS 4.0 vulnerability scans, execute GDPR 'Right to be Forgotten' customer data anonymization requests, audit credit card PAN masking, and export compliance certificates.",
            layout="PCI-DSS / GDPR Compliance Control Panel (Scan Type [PCI-DSS Vulnerability / GDPR Data Anonymization / Credit Card PAN Masking], Target Customer ID, Data Deletion Reason), Automated Audit Results Canvas, Compliance Certification Log DataGrid.",
        ),
        name="security-pci-dss-gdpr-compliance-audit-manager",
    ),
    path(
        "security/system-security-privilege-management/",
        views.SecurityPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="15.5",
            screen_title="System Security Privilege Management",
            module_label="System Security",
            legacy_page="SystemSecurityPrivilege.aspx",
            tier="D",
            phase=12,
            purpose="To configure fine-grained role-based security permissions specifically for AES-256 key rotation, IP whitelist management, database disaster recovery restores, and GDPR data anonymization execution.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per Security Screen, Save/Reset Action Toolbar.",
        ),
        name="security-system-security-privilege-management",
    ),
]
