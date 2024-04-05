"""Script for running any/all command line tasks for this project.

All command line tasks should be defined in this file. The only
exception to this is managing dependencies.

All commands in this file assume you're in the root directory and
you've activated the virtual environment.
"""

# Invoke always requires a context parameter, even if it ends up going
# unused. As of this writing, there are a handful of tasks that don't
# use their context parameters.
# pylint: disable=unused-argument

# Built-in libraries:
import sys

# Third-party dependencies:
from dotenv import dotenv_values
from invoke import task

# Environment variable files:
ENV_TEMPLATE = ".env.template"
ENV_ACTUAL = ".env"

# Configs:
TEMPLATE_CONF = dotenv_values(ENV_TEMPLATE)
ACTUAL_CONF = dotenv_values(ENV_ACTUAL)

# Absolute paths to src and build directories:
SRC_DIR = f"{ACTUAL_CONF['HCI_ROOT_DIR']}/src"
BUILD_DIR = f"{ACTUAL_CONF['HCI_ROOT_DIR']}/build"


@task
def fmt(c):
    """Format code."""
    c.run("go fmt ./...")
    c.run("black tasks.py")


@task
def lint(c):
    """Run the linter."""
    c.run("go vet ./...")
    c.run("pylint tasks.py")


@task
def clean(c):
    """Remove old binary."""
    c.run(f"rm -rf {BUILD_DIR}/*")


@task
def build(c):
    """Build the binary."""
    c.run(f"go build -o {BUILD_DIR}/hci {SRC_DIR}")


@task
def test(c):
    """Run the test suite."""
    c.run("go test -cover ./...")


@task
def types(c):
    """Check types in the Python code."""
    c.run("mypy tasks.py")


@task
def envsame(c):
    """Ensure environment variable keys match."""
    if TEMPLATE_CONF.keys() != ACTUAL_CONF.keys():
        print(".env keys do not match. Check your .env files.")
        sys.exit(1)


@task(pre=[fmt, lint, clean, build, test, types, envsame])
def check(c):
    """Run pre-submit checks."""


@task
def dev(c):
    """Run the development server."""
    c.run(f"source {ENV_ACTUAL} && go run {SRC_DIR}/main.go")
