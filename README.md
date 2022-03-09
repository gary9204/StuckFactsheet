# Factsheet
Application to explore facts about algebraic structures.

## Description
Factsheet is an application to explore facts about algebraic structures.
Factsheet provides tools for constructing small sets, binary operations,
and groups.  The tools include checks for basic facts about the objects
you construct.

Factsheet consists of three Python packages: `factsheet`,
`factsheet_test`, and `factsheet_doc`.  Package `factsheet` contains
Python 3 application code, which uses Python
[bindings](https://lazka.github.io/pgi-docs/) for
[GTK](https://en.wikipedia.org/wiki/GTK) widgets.  Package
`factsheet_test` contains [pytest](https://docs.pytest.org/en/latest/)
unit tests.  Package `factsheet_doc` contains HTML documentation
generated with [Sphinx](https://www.sphinx-doc.org/en/master/).

Factsheet is a personal project.  The main purpose is to practice
software development including basic design, Python coding, testing,
documentation, configuration management, and publication.  In addition,
I hope to use Factsheet to satisfy my curiosity about near rings.

## Installation
Factsheet is not prepared for `pip` installation yet.  You can run the
application from a local copy of the repository using the bash command
line or the console in Eclipse.

I run and test Factsheet in a virtual environment consisting of the
following.

  * Linux (Debian 4.19.208-1 (2021-09-29) x86_64)
  * GNU bash, version 5.0.3(1)-release
  * Python 3.7.3
  * Python packages listed in [requirements.txt](./requirements.txt)
  * Environment configuration [pyvenv.cfg](./pyvenv.cfg)
  * Eclipse version 2021-12 (4.22.0)

## Usage
The following command runs Factsheet when executed from the `src/`
directory of the repository.

    python3 -m factsheet.app

I am refactoring Factsheet to address deficiencies in organization and
unnecessarily complex code.  Checkout tag `factsheet_first_look` for a
working, partial version of Factsheet.  Checkout branch `next` to see
current progress on refactoring.

## License
Factsheet is licensed under the GNU General Public License v3.0 with the
complete license in file [LICENSE](./LICENSE).

