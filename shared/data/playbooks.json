{
  "CRITICAL": {
    "playbook_id": "PB-CRIT-01",
    "steps": [
      "Isolate affected servers immediately from the main VPC subnet.",
      "Engage Incident Command Team and initiate P0 communication channel.",
      "Patch or rotate service credentials for affected machines."
    ]
  },
  "HIGH": {
    "playbook_id": "PB-HIGH-01",
    "steps": [
      "Restrict IP access at the security group level to authorized subnets only.",
      "Alert On-Call Security Engineer.",
      "Schedule vulnerability remediation path within 24 hours."
    ]
  },
  "MEDIUM": {
    "playbook_id": "PB-MED-01",
    "steps": [
      "Log activity and flag for regular update lifecycle.",
      "Verify mitigation controls are active in surrounding microservices."
    ]
  },
  "LOW": {
    "playbook_id": "PB-LOW-01",
    "steps": [
      "Record the event in the security audit log.",
      "Continue routine monitoring for repeated occurrences."
    ]
  },
  "RANSOMWARE": {
    "playbook_id": "PB-RANSOM-01",
    "steps": [
      "Disconnect infected endpoints from the network immediately.",
      "Preserve forensic evidence before remediation.",
      "Notify executive incident response stakeholders."
    ]
  },
  "SQL_INJECTION": {
    "playbook_id": "PB-SQLI-01",
    "steps": [
      "Block malicious requests using WAF rules.",
      "Review database logs for unauthorized queries.",
      "Patch vulnerable input validation logic."
    ]
  },
  "RCE": {
    "playbook_id": "PB-RCE-01",
    "steps": [
      "Terminate vulnerable application instances.",
      "Deploy emergency security patches.",
      "Verify system integrity before restoring services."
    ]
  },
  "XSS": {
    "playbook_id": "PB-XSS-01",
    "steps": [
      "Sanitize affected user-generated content.",
      "Invalidate active user sessions.",
      "Deploy updated content security policies."
    ]
  },
  "DOS": {
    "playbook_id": "PB-DOS-01",
    "steps": [
      "Enable traffic rate limiting.",
      "Scale infrastructure to absorb excess traffic.",
      "Block abusive source IP addresses."
    ]
  },
  "PATH_TRAVERSAL": {
    "playbook_id": "PB-PATH-01",
    "steps": [
      "Disable vulnerable file endpoints.",
      "Audit file access logs for suspicious requests.",
      "Deploy path normalization validation."
    ]
  },
  "PRIVILEGE_ESCALATION": {
    "playbook_id": "PB-PRIV-01",
    "steps": [
      "Disable compromised user accounts.",
      "Rotate privileged credentials immediately.",
      "Audit administrative actions performed recently."
    ]
  },
  "SSRF": {
    "playbook_id": "PB-SSRF-01",
    "steps": [
      "Block outbound requests to internal metadata services.",
      "Inspect application logs for suspicious destinations.",
      "Apply network segmentation controls."
    ]
  },
  "AUTH_BYPASS": {
    "playbook_id": "PB-AUTH-01",
    "steps": [
      "Force logout of active user sessions.",
      "Rotate authentication signing keys.",
      "Review identity provider logs."
    ]
  },
  "DATA_LEAK": {
    "playbook_id": "PB-DATA-01",
    "steps": [
      "Restrict external access to exposed resources.",
      "Identify affected customer records.",
      "Notify compliance and legal response teams."
    ]
  },
  "MALWARE": {
    "playbook_id": "PB-MAL-01",
    "steps": [
      "Quarantine infected hosts from the corporate network.",
      "Run endpoint detection and response scans.",
      "Restore affected systems from trusted backups."
    ]
  },
  "INSIDER_THREAT": {
    "playbook_id": "PB-INS-01",
    "steps": [
      "Revoke all active sessions and disable the insider's Active Directory account.",
      "Audit access logs to determine systems accessed and files downloaded.",
      "Engage HR and Legal departments to initiate formal internal investigation."
    ]
  },
  "API_ABUSE": {
    "playbook_id": "PB-API-01",
    "steps": [
      "Identify the source IP/API token abusing the endpoint and apply rate limits or block them.",
      "Inspect API logs to determine scope of data accessed or modified.",
      "Update API Gateway security rules to enforce stricter payload validation."
    ]
  },
  "SUPPLY_CHAIN": {
    "playbook_id": "PB-SUPP-01",
    "steps": [
      "Pin vendor package versions to known-safe releases and roll back the affected build.",
      "Audit build environment and artifact repository for unauthorized modifications.",
      "Establish a secure clean-room rebuild of all pipeline components."
    ]
  },
  "KUBERNETES_ATTACK": {
    "playbook_id": "PB-K8S-01",
    "steps": [
      "Isolate the compromised pod or node using network policies and label selectors.",
      "Inspect Kubernetes API server audit logs for unauthorized configuration changes.",
      "Re-deploy the workload with non-root privileges and updated security context."
    ]
  },
  "CLOUD_MISCONFIG": {
    "playbook_id": "PB-CLOUD-01",
    "steps": [
      "Modify the cloud resource configuration to align with the secure baseline baseline policy.",
      "Review IAM change history logs to identify the user/role that applied the change.",
      "Scan adjacent cloud services for similar configuration drift."
    ]
  },
  "CONTAINER_ESCAPE": {
    "playbook_id": "PB-ESC-01",
    "steps": [
      "Drain and cordon the affected Kubernetes node to prevent scheduling new workloads.",
      "Terminate all running containers on the compromised host immediately.",
      "Update container runtime and kernel to patch sandbox escape vulnerability."
    ]
  },
  "DNS_HIJACK": {
    "playbook_id": "PB-DNS-01",
    "steps": [
      "Restore DNS records to authoritative state at the external registrar.",
      "Rotate registrar login credentials and enable mandatory multi-factor authentication.",
      "Flush local and corporate DNS resolver caches to purge poisoned entries."
    ]
  },
  "CREDENTIAL_STUFFING": {
    "playbook_id": "PB-CRED-01",
    "steps": [
      "Implement IP rate limiting and CAPTCHA challenge on the login endpoint.",
      "Identify successfully matched accounts and force immediate password resets.",
      "Notify affected users regarding unauthorized access attempts on their accounts."
    ]
  },
  "PHISHING": {
    "playbook_id": "PB-PHISH-01",
    "steps": [
      "Purge the phishing email from all user mailboxes using Microsoft 365 or Google Workspace admin tools.",
      "Block the sender domain and malicious link URLs at the email gateway.",
      "Force credential reset and session revocation for users who clicked the link."
    ]
  },
  "OAUTH_ABUSE": {
    "playbook_id": "PB-OAUTH-01",
    "steps": [
      "Revoke the malicious OAuth application token from the identity provider.",
      "Inspect OAuth consent history and audit logs for unauthorized API calls.",
      "Update OAuth consent policies to restrict third-party app scopes."
    ]
  },
  "LATERAL_MOVEMENT": {
    "playbook_id": "PB-LAT-01",
    "steps": [
      "Deploy host-based firewall rules to restrict internal East-West traffic.",
      "Rotate administrative credentials across the affected network segment.",
      "Deploy honeytokens or network sensors to detect further credential harvesting."
    ]
  },
  "CRYPTO_MINER": {
    "playbook_id": "PB-MINE-01",
    "steps": [
      "Terminate unauthorized processes and remove persistence mechanisms on infected hosts.",
      "Block outbound connections to known mining pools at the egress firewall.",
      "Audit resource utilization thresholds and configure automatic container CPU limits."
    ]
  },
  "WEB_SHELL": {
    "playbook_id": "PB-SHELL-01",
    "steps": [
      "Delete the web shell script file from the application directory.",
      "Inspect web server logs to locate the initial upload vector and patch the vulnerability.",
      "Rotate all application secrets and database credentials accessed by the web shell."
    ]
  },
  "PERSISTENCE": {
    "playbook_id": "PB-PERS-01",
    "steps": [
      "Identify and remove rogue cron jobs, registry keys, or scheduled tasks.",
      "Audit local user accounts and authorized SSH keys to delete unauthorized entries.",
      "Reboot the system into a validated, clean state and monitor startup items."
    ]
  },
  "FILELESS_MALWARE": {
    "playbook_id": "PB-FILELESS-01",
    "steps": [
      "Isolate the host and dump memory to preserve evidence of running processes.",
      "Terminate parent processes executing suspicious PowerShell, WMI, or cmd commands.",
      "Apply restrictive script execution policies and enable AMSI logging."
    ]
  },
  "ROGUE_ADMIN": {
    "playbook_id": "PB-ROGUE-01",
    "steps": [
      "Revoke all administrative access keys, passwords, and API tokens of the rogue account.",
      "Enforce strict dual-authorization dual-authorization controls for subsequent administrative actions.",
      "Revert all unauthorized infrastructure and policy changes made by the admin."
    ]
  },
  "ZERO_DAY": {
    "playbook_id": "PB-ZERO-01",
    "steps": [
      "Deploy temporary virtual patching rules at the WAF or IPS level.",
      "Enable advanced logging and isolate high-value assets hosting the vulnerable software.",
      "Coordinate with the software vendor to acquire and test the hotfix."
    ]
  },
  "SECRET_LEAKAGE": {
    "playbook_id": "PB-SECL-01",
    "steps": [
      "Revoke and rotate the exposed secrets, API keys, or database credentials immediately.",
      "Remove the secret file from repository history using git rewrite tools.",
      "Review access logs for the leaked credentials to detect unauthorized actions."
    ]
  },
  "S3_EXPOSURE": {
    "playbook_id": "PB-S3-01",
    "steps": [
      "Update the S3 bucket access control list and block public access policy.",
      "Review bucket access logs to determine if any sensitive data was downloaded.",
      "Configure automated guardrails to prevent public bucket creation in the future."
    ]
  },
  "REDIS_EXPOSURE": {
    "playbook_id": "PB-REDIS-01",
    "steps": [
      "Configure Redis to bind only to local interfaces and enable password authentication.",
      "Terminate active unauthorized client connections and flush transient cache data.",
      "Review commands executed via MONITOR command to identify data exposure scope."
    ]
  },
  "ELASTICSEARCH_EXPOSURE": {
    "playbook_id": "PB-ELAST-01",
    "steps": [
      "Enable cluster security and configure user authentication for Elasticsearch.",
      "Restrict port 9200 access at the network firewall to authorized IP ranges.",
      "Audit cluster log history to verify if index snapshots were modified."
    ]
  },
  "VPN_COMPROMISE": {
    "playbook_id": "PB-VPN-01",
    "steps": [
      "Revoke the affected VPN client certificate and terminate all active sessions.",
      "Perform immediate malware scan on the user's remote endpoint.",
      "Enforce device posture checks and multi-factor authentication for all VPN logins."
    ]
  },
  "DDOS": {
    "playbook_id": "PB-DDOS-01",
    "steps": [
      "Divert traffic through a cloud-based DDoS mitigation scrub service.",
      "Enable Geoblocking and rate limiting for non-essential traffic sources.",
      "Collaborate with upstream ISP to filter traffic closer to the source."
    ]
  },
  "SQLI": {
    "playbook_id": "PB-SQLI-02",
    "steps": [
      "Block SQL injection attempts by deploying custom WAF rules.",
      "Review database query logs to verify if data exfiltration occurred.",
      "Update database schemas to use parameterized queries in affected endpoints."
    ]
  },
  "LDAP_INJECTION": {
    "playbook_id": "PB-LDAP-01",
    "steps": [
      "Implement input validation and LDAP query parameter escaping in the application code.",
      "Inspect active directory logs to verify if password hashes were exposed.",
      "Restrict network connectivity from application servers to the LDAP directory."
    ]
  },
  "COMMAND_INJECTION": {
    "playbook_id": "PB-COMM-01",
    "steps": [
      "Disable system command execution capabilities in the web application.",
      "Perform full system integrity scan on the affected host for backdoor processes.",
      "Redeploy the application service from a clean repository image."
    ]
  },
  "CSRF": {
    "playbook_id": "PB-CSRF-01",
    "steps": [
      "Enforce anti-CSRF tokens for all state-changing HTTP requests.",
      "Configure cookie attributes with SameSite=Strict and Secure flags.",
      "Log out all active user sessions to clear potentially hijacked contexts."
    ]
  },
  "XXE": {
    "playbook_id": "PB-XXE-01",
    "steps": [
      "Disable external entity resolution (DTD) in all XML parser configurations.",
      "Inspect system outbound logs to see if files were exfiltrated via external endpoints.",
      "Configure local firewalls to block unauthorized outbound connections from XML parsers."
    ]
  },
  "OPEN_REDIRECT": {
    "playbook_id": "PB-REDIRECT-01",
    "steps": [
      "Enforce a strict whitelist of allowed redirect URLs in the redirection controller.",
      "Sanitize redirect parameters to prevent injection of malicious schemes.",
      "Deploy a warning page alerting users they are leaving the trusted domain."
    ]
  },
  "PROTOTYPE_POLLUTION": {
    "playbook_id": "PB-POLLUTE-01",
    "steps": [
      "Update Javascript libraries to patched versions and deploy object freeze patterns.",
      "Inspect application memory for altered built-in object prototypes.",
      "Redeploy backend Node.js microservices to clear polluted memory spaces."
    ]
  },
  "DIRECTORY_TRAVERSAL": {
    "playbook_id": "PB-DIR-01",
    "steps": [
      "Implement strict path sanitization and normalization checks on file paths.",
      "Restrict file system permissions of the web application user to minimal paths.",
      "Verify file system logs to see what configuration or system files were read."
    ]
  },
  "FILE_INCLUSION": {
    "playbook_id": "PB-INCL-01",
    "steps": [
      "Disable dynamic file inclusion configurations such as PHP's allow_url_include.",
      "Whitelist specific local files allowed for inclusion in the template engine.",
      "Perform code review of all file rendering controllers in the repository."
    ]
  },
  "WEAK_ENCRYPTION": {
    "playbook_id": "PB-CRYPT-01",
    "steps": [
      "Upgrade encryption protocols to TLS 1.3 and deprecate obsolete algorithms.",
      "Regenerate and redeploy SSL certificates using modern cipher suites.",
      "Re-encrypt historical database columns using AES-256-GCM."
    ]
  },
  "JWT_FAILURE": {
    "playbook_id": "PB-JWT-01",
    "steps": [
      "Update JWT parser configuration to reject the 'none' algorithm and enforce signature checks.",
      "Rotate JWT signing keys immediately and invalidate existing tokens.",
      "Deploy token blacklist verification at the API gateway layer."
    ]
  },
  "SESSION_FIXATION": {
    "playbook_id": "PB-SESS-01",
    "steps": [
      "Implement automatic session ID regeneration upon successful authentication.",
      "Invalidate old session identifiers on both client and server sides.",
      "Enforce short-lived session timeouts for active connections."
    ]
  },
  "RACE_CONDITION": {
    "playbook_id": "PB-RACE-01",
    "steps": [
      "Introduce pessimistic locking or mutex synchronization mechanisms in the database transaction block.",
      "Audit transaction history logs to reconcile account balances and state discrepancies.",
      "Re-run test scenarios with concurrent threads to validate the race fix."
    ]
  },
  "DESERIALIZATION": {
    "playbook_id": "PB-DESER-01",
    "steps": [
      "Replace native serialization libraries with safe formats like JSON or Protocol Buffers.",
      "Configure look-ahead deserialization filters to whitelist permitted classes.",
      "Isolate deserialization workers in restricted sandbox environments."
    ]
  },
  "OAUTH_MISCONFIG": {
    "playbook_id": "PB-OAUTH-02",
    "steps": [
      "Enforce strict redirect URI matching and require state parameter validation in OAuth flow.",
      "Review client application registrations in the identity provider console.",
      "Revoke active authorization codes issued during the anomaly window."
    ]
  },
  "ACCESS_CONTROL_BREACH": {
    "playbook_id": "PB-ACCESS-01",
    "steps": [
      "Deploy role-based access control (RBAC) validations at the API controller level.",
      "Inspect access logs to trace resources accessed during the breach.",
      "Invalidate current session tokens of the exploiting user account."
    ]
  },
  "BOLA": {
    "playbook_id": "PB-BOLA-01",
    "steps": [
      "Implement ownership validation checks mapping user identities to requested resource IDs.",
      "Perform full vulnerability audit of REST API resource lookup endpoints.",
      "Deploy rate limiting rules to block sequential ID enumerations."
    ]
  },
  "PORT_SCAN": {
    "playbook_id": "PB-SCAN-01",
    "steps": [
      "Configure host firewall to drop traffic from scanning IP addresses.",
      "Identify and close unneeded open ports on public-facing assets.",
      "Review network flow logs to ensure scans did not discover hidden endpoints."
    ]
  },
  "MALICIOUS_FILE_UPLOAD": {
    "playbook_id": "PB-UPLOAD-01",
    "steps": [
      "Store uploaded files in a dedicated non-executable container bucket.",
      "Scan all incoming file uploads with antivirus tools and verify extensions.",
      "Disable file execution permissions on storage directories."
    ]
  },
  "DNS_AMPLIFICATION": {
    "playbook_id": "PB-DNSAMP-01",
    "steps": [
      "Configure DNS resolver to disable recursion for external IP requests.",
      "Deploy response rate limiting (RRL) on the authoritative DNS servers.",
      "Collaborate with DDoS mitigation vendor to filter incoming UDP port 53 flood."
    ]
  },
  "BEACONING": {
    "playbook_id": "PB-BEACON-01",
    "steps": [
      "Identify the internal host generating regular outbound heartbeat connections.",
      "Block the Command & Control (C2) domain at the secure web gateway.",
      "Isolate the infected host and trigger full endpoint response scan."
    ]
  },
  "SECRET_EXPOSURE": {
    "playbook_id": "PB-SECRET-02",
    "steps": [
      "Revoke the leaked credential or API key on the external service provider portal.",
      "Audit log files to ensure secrets are redacted before writing to disk.",
      "Perform an automated scan of internal wikis and documents for other exposed secrets."
    ]
  }
}