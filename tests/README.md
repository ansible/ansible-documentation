# Descriptions of requirements files

The following table explains the purpose of the `.in` and `.txt` files in the `tests/` directory of this repository:

| File            | Purpose                                                                                            | 
| ----            | -------                                                                                            |
|constraints.in   | Pins for the stable, tested versions of sphinx and antsibull-docs that production builds rely upon |
|formatters.in    | List of Formatters required                                                                        |
|pip-compile.in   | Pin vesrion of `uv` for `pip-compile` nox session                                                  |
|pr_labeler.in    | Requirements for pr_labeler                                                                        |
|requirements.in  | Requirements file for Docs Build                                                                   |
|spelling.in      | Requirements for `spelling` nox session                                                            |
|static.in        | Requirements for `static` nox session                                                              |
|tag.in           | Requirements for `tag` nox session                                                                 |
|typing.in        | Requirements for `typing` nox session                                                              |
|formatters.txt   | Output of `uv pip compile --universal --output-file tests/formatters.txt -r tests/formatters.in`   |
|pip-compile.txt  | Output of `uv pip compile --universal --output-file tests/pip-compile.txt tests/pip-compile.in`    |
|pr_labeler.txt   | Output of `uv pip compile --universal --output-file tests/pr_labeler.txt tests/pr_labeler.in `     |
|requirements.txt | Output of `uv pip compile --universal --output-file tests/requirements.txt tests/requirements.in`  |
|spelling.txt     | Output of `uv pip compile --universal --output-file tests/spelling.txt tests/spelling.in`          |
|static.txt       | Output of `uv pip compile --universal --output-file tests/static.txt tests/static.in`              |
|tag.txt          | Output of `uv pip compile --universal --output-file tests/tag.txt tests/tag.in`                    |
|typing.txt       | Output of `uv pip compile --universal --output-file tests/typing.txt tests/typing.in`              |
