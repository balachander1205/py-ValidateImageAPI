title image validation api server
rem venv/Scripts/activate -exit
rem echo Starting image validation application
waitress-serve --port 5002 --host 0.0.0.0 --call app:app
rem python app.py
pause