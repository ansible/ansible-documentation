# Descriptions of requirements files

The following table explains the purpose of the `.in` and `.txt` files in the `tests/` directory of this repository:

| File            | Purpose                                                             | Pip Constraints file (when relevant) |
| ----            | -------                                                             | ------------------------------------ |
|constraints.in   | Pins for sphinx and antsibull-docs, version bounds for known issues | --                                   |
|formatters.in    | List of Formatters required                                         | formatters.txt                       |
|pip-compile.in   | Pin vesrion of `uv` for `pip-compile` nox session                   | pip-compile.txt                      |
|pr_labeler.in    | Requirements for pr_labeler                                         | pr_labeler.txt                       |
|requirements.in  | Requirements file for Docs Build                                    | requirements.txt                     |
|spelling.in      | Requirements for `spelling` nox session                             | spelling.txt                         |
|static.in        | Requirements for `static` nox session                               | static.txt                           |
|tag.in           | Requirements for `tag` nox session                                  | tag.txt                              |
|typing.in        | Requirements for `typing` nox session                               | typing.txt                           |
