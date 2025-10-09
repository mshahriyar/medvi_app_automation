## ⚙️ Project Setup Guide (macOS / Linux)

Follow these steps to set up and run the **MEDVI App Automation Project** safely on a new machine.

---

### 🧩 1. Install Python (via Homebrew)
If Python is not installed, run:
```bash
brew install python
If you see a permissions error such as
Error: /opt/homebrew/Cellar is not writable,
fix it by granting ownership of the Homebrew directory:

bash
Copy code
sudo chown -R $(whoami) /opt/homebrew
chmod u+w /opt/homebrew
Then verify installation:

bash
Copy code
python3 --version
pip3 --version
🧱 2. Create and Activate a Virtual Environment
From the project root folder (where requirements.txt exists):

bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
You should now see:

scss
Copy code
(.venv) username@MacBook % 
🧰 3. Upgrade pip and Install Dependencies
Inside the virtual environment:

bash
Copy code
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
🧪 4. Install Playwright Browsers
Only required once (downloads Chromium, Firefox, WebKit):

bash
Copy code
playwright install
🧭 5. Verify Environment
Run the following to confirm everything is installed correctly:

bash
Copy code
which python
which pip
python --version
pip --version
Both paths should point inside your .venv directory.

🚀 6. Run Tests
Execute all tests with:

bash:
pytest -v -s

Install playwright with pytest:
pip install pytest-playwright

Verify:
pytest --fixtures | grep page

Playwright:
playwright install
