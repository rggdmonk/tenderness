---
icon: lucide/rocket
hide:
  - path
---

# Install

## Prerequisites

**tenderness** depends on [pycairo](https://pycairo.readthedocs.io/en/latest/getting_started.html) and [PyGObject](https://pygobject.gnome.org/getting_started.html), which require system libraries before installing. 

## Virtual environment

[uv](https://docs.astral.sh/uv/) is recommended, but any virtual environment manager works.

=== "uv"
    ```bash
    uv venv --python 3.13
    source .venv/bin/activate
    ```

## tenderness

=== "uv"

    ```bash
    uv pip install tenderness
    ```
=== "pip"

    ```bash
    pip install tenderness
    ```