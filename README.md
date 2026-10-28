Lab 5: Static Code Analysis - Movie Review and Rating System

Source repository: https://github.com/SETAPESU26/L5_33_movie_reviews
Original commit: 780810d
Submission branch: lab5-static-analysis

movie_reviews.py is the corrected program.
issues.md contains the required issue documentation table, with original line numbers.
reports/before contains the three original analyzer reports and demo output.
reports/after contains the three final analyzer reports, demo output, and test output.
reports/stages contains evidence from the separate Pylint and Bandit fix stages.
Each report directory also records commands and exit codes. Analyzer stderr is saved separately.

Results (before -> after):
Pylint: 5.47/10 -> 10.00/10
Bandit: 4 findings (1 High, 1 Medium, 2 Low) -> 0 findings
Flake8: 4 findings -> 0 findings
Regression tests: 8 passed

Flake8 reports are empty when there are no findings; its final exit code is 0.
The analyzers target movie_reviews.py, as required by the lab. No rules are disabled.
Pylint uses --persistent=n to avoid cached scores; Bandit uses explicit text output.

Changes are split into exactly three commits after the original commit:
1. fix: resolve Pylint quality and maintainability findings
2. fix: resolve all Bandit security findings
3. fix: resolve Flake8 formatting and document verified results

The submission package includes a Git bundle, commit_history.txt with full commit IDs,
and three individual patches. The Git bundle preserves the original commit and all
three new commits. It can be cloned without GitHub access.

To restore the committed repository from the package directory:
git clone L5_33_movie_reviews.bundle restored_movie_reviews
cd restored_movie_reviews

To reproduce the checks from the repository directory:
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-analysis.txt
.venv/bin/python movie_reviews.py
.venv/bin/python -m pylint --persistent=n movie_reviews.py
.venv/bin/python -m bandit -r movie_reviews.py -f txt
.venv/bin/python -m flake8 movie_reviews.py
.venv/bin/python -m unittest -v test_movie_reviews.py

To regenerate the final analyzer reports:
.venv/bin/python -m pylint --persistent=n movie_reviews.py > reports/after/pylint_report.txt
.venv/bin/python -m bandit -r movie_reviews.py -f txt > reports/after/bandit_report.txt
.venv/bin/python -m flake8 movie_reviews.py > reports/after/flake8_report.txt

Expected output changes:
The streaming address is now 127.0.0.1:8000. The script only displays this address;
it does not start a streaming server. The unused moderator password is removed.
Review IDs are deterministic 64-character SHA-256 digests rather than 10-character
MD5 prefixes. They identify review content; they are not authentication tokens.
The featured movie still varies, now using secrets.choice. Helper functions now use
snake_case, and importing the module no longer executes the demo.
Ratings, average calculations, rankings, optional reviews, and genres are preserved.

Reflection questions were absent from the supplied handout. They are omitted as
instructed by the user; no substitute questions or answers have been invented.

The three commits are available on the personal GitHub fork:
https://github.com/Audatic07/L5_33_movie_reviews/tree/lab5-static-analysis
