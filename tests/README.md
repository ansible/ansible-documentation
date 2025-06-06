# Descriptions of requirements files

The following table explains the purpose of the `.in` and `.txt` files in the `tests/` directory of this repository:

| File            | Purpose                                                             | Pip Constraints file (when relevant) |
| ----            | -------                                                             | ------------------------------------ |
|constraints.in   | Pins/version bounds for sphinx and antsibull-docs  for known issues | --                                   |
|formatters.in    | List of Formatters required                                         | formatters.txt                       |
|pip-compile.in   | Dependencies for `pip-compile` nox session                          | pip-compile.txt                      |
|pr_labeler.in    | Dependencies for pr_labeler                                         | pr_labeler.txt                       |
|requirements.in  | Dependencies file for Docs Build                                    | requirements.txt                     |
|spelling.in      | Dependencies for `spelling` nox session                             | spelling.txt                         |
|static.in        | Dependencies for `static` nox session                               | static.txt                           |
|tag.in           | Dependencies for `tag` nox session                                  | tag.txt                              |
|typing.in        | Dependencies for `typing` nox session                               | typing.txt                           |
