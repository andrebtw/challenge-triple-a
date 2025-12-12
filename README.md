# challenge-triple-a

This is a small Flask-based dashboard that shows system metrics (CPU, memory, network, processes, and file stats) with a simple responsive UI.

## Quick start
1. Install Python (3.9+ recommended).
2. Create a virtual environment (optional but recommended):
   - Windows (PowerShell): `python -m venv .venv ; .\.venv\Scripts\Activate`
3. Install dependencies:
   - `pip install flask psutil`
4. Run the app:
   - `python app.py`
5. Open your browser at the address printed in the terminal (usually `http://127.0.0.1:5000/`).

## Project structure
- `monitory.py` — Function container.
- `template/index.html` — Page template with placeholders for data.
- `static/style.css` — Styles for the dashboard.
- `app.py` — Flask app that collects and serves system data.

## Notes
- The nav links jump to each section on the page.


