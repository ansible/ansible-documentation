Thanks for your contribution, @{{ ctx.member.user.login }}! Please make sure that your {{ ctx.TYPE }} includes sufficient and meaningful details in the description.
{% if ctx.TYPE == "pull request" %}
PR descriptions provide important context and allow other developers and our future selves to understand a change's rationale and what it actually fixes or accomplishes.
{% else %}
Issue descriptions are important so others can fully understand and reproduce the issue.
{% endif %}
<!--- boilerplate: no_body_nag --->
