# Ohjelmistotekniikka, harjoitustyö

This is the project work for course Ohjelmistotekniikka.

**Membership payment card project description**


The application is built to allow storekeepers and staff to offer a membership payment card solution to customers, who can benefit discounts by using the membership payment card solution. It helps to retain long-term customer loyalty, provides user-friendly cash and card payment experience, support customers to keep track of completed purchases, and streamline storekeeper's transaction management.


**Documentation**

[link to User Instructions document](dokumentaatio/Instructions.md)


[link to Specification document](dokumentaatio/specification.md)


[link to Working hour document](dokumentaatio/workhour.md)


[link to Architecture Description document](dokumentaatio/architecture.md)


[link to changelog document](dokumentaatio/changelog.md)


**Release**


[link to Week 5 release](https://github.com/xiongxiaowen/ot-harjoitustyo/releases/tag/Viikko5)


[link to Week 6 release](https://github.com/xiongxiaowen/ot-harjoitustyo/releases/tag/Viikko6)


**Installation**


Install dependencies with the command:
- poetry install


Start the application with the command:
- poetry run invoke start


**Command Line Functions**


Running the Program with the command:
- poetry run invoke start


Testing are run with the command:
- poetry run invoke test


Test Coverage report can be generated  with the command:
- poetry run invoke coverage-report (The html report will be generated in the htmlcov directory)
- poetry run coverage html (view HTML report via link)


Pylint, run the checks defined in the .pylintrc file with the command:
- poetry run invoke lint