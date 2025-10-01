## Setup For New Developers
This course and project brings together people of varying proficiency and to serve as a point of reference for my classmates, I have compiled the following outline. - John P.

### How do I set it up?

This repository already contains the required elements (so don't do it again!) but for other groups using this as a reference (and for my future self), the process is outlined farther down in the file.


### How to get the code

1. Make sure you have the basic tools installed on your system including python, git, and uv.

2. Set up your GitHub access and then clone the repository.

```bash
git clone git@github.com:John-Popovici/MCYSD-19-escape-room.git
```

3. Set up the environment using uv. This generates `.venv` based off of information from `.python-version` and `pyproject.toml`.

```bash
uv sync
```

4. Run the project files, linting, and testing.

```bash
uv run src/main.py # run the main python file
uv run ruff check # run ruff for linting
uv run pytest # run pytest for testing
```


### How to contribute

1. Make sure you have your IDE of choice such as VSCodium or VSCode with appropriate extensions.

2. Change to a branch to contribute to the codebase. If you do not have a branch, you can create one, or otherwise move to it.

```bash
git branch # see branches as well as current branch
git branch my-new-branch # create new branch, my-new-branch
git checkout my-new-branch # move to the branch, my-new-branch
```

3. Throughout development you can commit work.

```bash
git branch # double check what branch you are in
git add * # add all or specific files
git commit -m "comment" # commit the changes. Add an informative but short comment about the commit
git push # sends the commit to GitHub
```

4. Test your work done using `pytest` and `ruff`.
	- Tests will have to be updated throughout the assignment as we learn more.
	- I recommend also using the ruff extension for an easier time.
	- Note that GitHub has been configured to run these tests on merge requests as well.

5. When looking to merge back into main, make sure to pull the latest main into your local branch in case it has since updated and fix conflicts if any arise.

```bash
git branch # double check what branch you are in
git pull origin main # merge the master into your branch
# fix conflicts if any
git push # sends the commit to GitHub
```

6. To merge into main, create a new pull request through the GitHub website.
	- There are other ways to do it, but this is most convenient.
	- It allows us to keep an eye on requests, comments, and GitHub actions.
	- If changes need to be further made before merging, repeat the above process.


### How do I set it up? Continued

1. Make sure you have the basic tools installed on your system including python, git, and uv.

```bash
uv init # create the project
uv venv

uv sync # set up the environment

uv run main.py # you can now run code
```

2. You can also add testing and linting using the following. Note the `--dev` is not required, but it doesn't hurt to do it better this way.

```bash
uv add --dev pytest
uv add --dev ruff
uv add --dev pytest-cov

uv sync # to update the environment
```

3. Note that your `pyproject.toml` will have to be updated depending on your project requirements and structure. This is an example file.

```toml
[project]
name = "mcysd-19-escape-room"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.4.2",
    "pytest-cov>=7.0.0",
    "ruff>=0.13.2",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v -s"

[tool.ruff.lint]
select = [
    # pep8-naming
    "N",
]
```

4. To get your local repository on GitHub, do the following.

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <url>
git branch -M main
git push -u origin main
```

5. To set up CI/CD and use github actions to run `pytest` and `ruff` you can create the following file `.github/workflows/run_test.yml`. Note that this is configured to run manually or on merge requests to main, but it can be configured to run on all pushes.

```yml
name: Run Pytest and Ruff

on:
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version-file: ".python-version"

      - name: Install uv
        uses: astral-sh/setup-uv@v6

      - name: Install the project
        run: uv sync --locked --all-extras --dev

      - name: Run Pytest
        run: uv run pytest --cov=src tests/

      - name: Run Ruff
        if: success() || failure()
        run: uv run ruff check . --output-format=github
```