@echo off
echo 🔹 Installing requirements...
pip install -r requirements.txt

echo 🔹 Running migrations...
python manage.py migrate

echo 🔹 Starting server in background...
start /B python manage.py runserver

echo 🔹 Opening browser...
start http://127.0.0.1:8000

echo ✅ Server started successfully!
