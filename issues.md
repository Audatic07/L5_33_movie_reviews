Line numbers refer to the original movie_reviews.py at commit 780810d.
Bandit severities are its reported severities; Pylint categories are convention, refactor, or warning.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Bandit B324: weak MD5 | Security, High | 46 | MD5 produces the review ID, truncated to 10 hex characters. Concatenating the two fields also makes different input pairs indistinguishable. | Use full SHA-256 over a JSON array of the two fields. IDs now contain 64 hex characters. |
| Bandit B104: all interfaces | Security, Medium | STREAM_HOST is 0.0.0.0. If used for a server, this would expose it on every interface. This demo only prints the address. | Set the default to 127.0.0.1 for local access. |
| Bandit B105: hard-coded password | Security, Low | An unused moderator password is stored in the source. | Remove the unused constant. There is no authentication consumer in this program. |
| Bandit B311: random.choice | Security, Low | Bandit flags the standard random generator. Featured movie selection is not security sensitive, but the lab requires every Bandit finding to be resolved. | Use secrets.choice while preserving selection from registered titles. |
| Pylint C0114/C0116: missing documentation | Convention | 1; 11, 16, 26, 34, 39, 45, 48, 54, 58 | The module and all nine functions lack docstrings. | Add short module and function docstrings. |
| Pylint C0103: naming | Convention | 8, 11, 16, 26, 34, 39, 45, 48, 54 | Function names and reviewText use mixed case; featured is also flagged. | Rename functions and review_text to snake_case, update every caller, and remove unused featured state. |
| Pylint W0603: global statement | Warning | 40-42 | Choosing a featured movie reassigns a module global that no caller reads. | Return the selected title directly without global reassignment. |
| Pylint R1705: unnecessary else | Refactor | 28-31 | The else branch follows a return and adds unnecessary nesting. | Return 0.0 after the conditional. |
| Pylint C0200: indexed iteration | Convention | 49-51 | A copied title list is traversed using range(len(...)). | Iterate with enumerate(movies, start=1). |
| Flake8 E225/E231: whitespace | Style | 35, 72 | Missing spaces around assignment and after a comma. | Insert the required spaces. |
| Flake8 E302/E261: spacing | Style | 48, 70 | A top-level function lacks a blank line and an inline comment has too few preceding spaces. | Add two blank lines between functions and two spaces before the comment. Wrap new long lines to satisfy the 79-character limit. |

Additional change: put main() behind the standard __name__ guard so importing the module does not execute the demo or populate movie data. This was found during review, not reported by the three tools.

Final verification: Pylint 10.00/10, Bandit 0 findings, Flake8 0 findings, and 8 passing regression tests. No analyzer rules were disabled and no findings were suppressed.
