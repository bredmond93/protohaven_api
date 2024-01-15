# protohaven_api
API system for protohaven

## Setup

### Configuration

This module requires a `config.yaml` file to run - chat with other protohaven devs to receive a copy.

### pre-commit

This repo uses pre-commit to autoformat and lint code. Ensure it's set up by following the instructions at https://pre-commit.com/#installation.

**Note: you must activate the virtualenv for pylint to properly run on pre-commit**. This is because it does dynamic checking of modules and needs
those modules to be loaded or else it raises module import errors.

## Running server locally

**There is currently no staging instance for integrations - actions taken on a local server will affect production.**

```
# Set up the environment
source venv/bin/activate
pip install -e .

# Run the server
python3 -m protohaven_api.main
```

## Running the CLI

```
# Set up the environment
source venv/bin/activate
pip install -e .


# Run the command
python3 -m protohaven_api.cli project_requests
```
