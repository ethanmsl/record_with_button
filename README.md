# record_with_button

## Auto-Documentation Link
To activate:
- In GitHub repo go to `settings > pages` Under `Build and deployment` set `Source` to **GitHub Actions**.
- Run the GitHub Action *or* make any commit to repository
- A new page will be created. Yay!
    - You can place that address in the above link for easy reader navigation.


## Dev-Dependencies Specified
- formatting: `isort` & `black`
- linting: `pylint`
- lsp & typechecking: `pyright`
- testing: `pytest` + `coverage` (via `pytest-cov`)
- auto-documentation: `pdoc` (*not* ~~"pdoc3"~~, which should be strongly avoided)


## Run Pre-Commit Hook Manually
from anywhere in project:
```zsh
poetry shell
git hook run pre-commit
```
