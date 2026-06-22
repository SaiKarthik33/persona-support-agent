\# API Troubleshooting \& Integration Guide



\## Authentication Requirements

All API endpoints require a Bearer token for authorization. 

\- \*\*Header Parameter:\*\* `Authorization: Bearer <AQ.Ab8RN6IKmh4eDKGr8yRvgoYjn\_Fls0XLs7xMYP7nHKKCg0iaeA>`

\- \*\*Content-Type:\*\* `application/json`

If you experience a 401 Unauthorized block, check that your token is not expired and is included in the headers correctly.



\## Common Interface Issues

If the user interface or dashboard is failing to load for over an hour, it is often due to a stale cache. The immediate guide to clear cookies is to navigate to your browser settings, select "Privacy and Security", and choose "Clear browsing data." Ensure "Cookies and other site data" is checked before confirming.

