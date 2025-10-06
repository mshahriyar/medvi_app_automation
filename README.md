# madvi_automation_project

How to run the tests locally

1. Activate the virtual environment (zsh):

```bash
source /Users/shahriyar/Documents/madvi_automation_project/.venv/bin/activate
```

2. Install dependencies (if not already installed):

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers (required for tests that launch browsers):

```bash
python -m playwright install --with-deps
```

4. Run tests with pytest:

```bash
cd /Users/shahriyar/Documents/madvi_automation_project
pytest -vv
```

Options:
- To run headed (show browser UI) set `HEADLESS=0` and use the pytest-playwright plugin's configuration or environment variables as needed.
- If `pytest` is not found, ensure the venv is activated and `pytest` is installed into that environment.

Notes:
- `conftest.py` intentionally avoids custom Playwright fixtures. The project uses the `pytest-playwright` plugin which provides `page`, `context`, and `browser` fixtures. Use the plugin fixtures in tests.
