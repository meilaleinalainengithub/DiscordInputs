IF EXIST ".venv" (
    python "\src\discordbot.py"
) ELSE (
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
)