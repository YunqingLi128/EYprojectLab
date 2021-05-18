call env\Scripts\activate.bat
set FLASK_APP=backend
set FLASK_ENV=development
start /B flask run

cd frontend/projectlabdemp
start /B npm run dev
