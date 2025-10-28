1.	Which issues were the easiest to fix, and which were the hardest? Why?
Easiest issues- style and convention related issues, since they needed only minor edits and no structural changes.
Hardest issues- the ones that needed structural changes were the hardest  to fix since we had to make sure that the functionality remained intact.


2.	Did the static analysis tools report any false positives? If so, describe one example.
Yes, Pylint flagged a potential issue about “re-adding logging handlers” each time configure_logging() is called, even though in our workflow it’s called only once in main(). This warning is technically valid in general contexts but a false positive here because the code is not re-imported or executed multiple times during runtime.


3.	How would you integrate static analysis tools into your actual software development workflow? Consider continuous integration (CI) or local development practices.
Local development- using tools like pylint, flake8, and bandit as pre-commit hooks via Git (using pre-commit framework). This ensures every developer’s code passes basic style and security checks before committing changes.
Continuous Integration- Integrate these checks into the CI/CD pipeline using GitHub Actions, GitLab CI, or Jenkins. The pipeline would fail or warn if the Pylint score drops below a threshold (e.g., 9.0), enforcing consistent code quality across commits.


4.	What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?
Code Quality:
•	Pylint score rose from about 4.80 to 9.79.
•	No more major issues like eval, bare except, or mutable defaults — all high-risk patterns removed.
Readability:
•	Code follows consistent naming and docstring conventions.
•	Logging replaced print statements, producing clearer runtime information.
Robustness:
•	File handling and type validation prevent crashes due to bad input or corrupted files.
•	The new Inventory class encapsulates data safely and allows easier testing and scaling.
