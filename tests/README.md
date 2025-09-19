# Descriptions of requirements files

The following table explains the purpose of the `.in` and `.txt` files in the `tests/` directory of this repository:

| File            | Purpose                                                             | Pip Constraints file (when relevant) |
| ----            | -------                                                             | ------------------------------------ |
|constraints.in   | Pins/version bounds for sphinx and antsibull-docs  for known issues | --                                   |
|formatters.in    | List of Formatters required                                         | formatters.txt                       |
|pr_labeler.in    | Dependencies for the labeler workflow                               | pr_labeler.txt                       |
|requirements.in  | Dependencies for the Sphinx docs builds                             | requirements.txt                     |
|pip-compile.in   | Dependencies for the `pip-compile` nox session                      | pip-compile.txt                      |
|spelling.in      | Dependencies for the `spelling` nox session                         | spelling.txt                         |
|static.in        | Dependencies for the `static` nox session                           | static.txt                           |
|tag.in           | Dependencies for the `tag` nox session                              | tag.txt                              |
|typing.in        | Dependencies for the `typing` nox session                           | typing.txt                           |
