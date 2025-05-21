"""PyInstaller-friendly launcher for the Streamlit front-end.

Locates ``streamlit_app.py`` relative to *this* file and starts the
Streamlit dev-server in a sub-process, then opens the browser.

Usage::

    python -m audit_insight.app.launcher
"""

import os
import subprocess
import sys
import webbrowser


def launch_application() -> None:
    """Start the Streamlit application and open the default browser."""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(this_dir, "streamlit_app.py")

    if not os.path.exists(script):
        print(f"streamlit_app.py not found in {this_dir}", file=sys.stderr)
        return

    # Launch Streamlit in the background (shell=True for Windows PATH lookup)
    subprocess.Popen(f'streamlit run "{script}"', shell=True)
    webbrowser.open("http://localhost:8501")


if __name__ == "__main__":
    launch_application()
