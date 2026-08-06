# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Email: [your-email@example.com] with details
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix**: Dependent on severity (Critical: 72 hours, High: 1 week, Medium: 2 weeks)

## Security Measures in This Project

This project demonstrates DevSecOps best practices including:

- **SAST**: Bandit, Semgrep for static code analysis
- **Dependency Scanning**: pip-audit for known CVEs
- **Container Security**: Trivy image scanning, Hadolint
- **Secrets Detection**: Gitleaks pre-commit and CI scanning
- **DAST**: OWASP ZAP baseline scanning
- **IaC Security**: Checkov for infrastructure misconfigurations
