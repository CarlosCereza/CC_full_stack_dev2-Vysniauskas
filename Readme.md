 >> TASK1
To open Blog website simply double-click on index.html file in any directory.

Tested using Microsoft Edge browser yet should work with any.

 >> TASK2
To start API server:

1. Start local MySQL server at port 3306
2. Start CMD here in this folder
3. Run following commands:

api-env\Scripts\activate.bat
python -m pip install -r requirements.txt
set FLASK_APP=main.py
python -m flask run


You may test this Restfull API with Postman next. Methods(other return error code #405):

GET http://127.0.0.1:5000/api/posts/
GET http://127.0.0.1:5000/api/posts/<id>
POST http://127.0.0.1:5000/api/posts/
DELETE http://127.0.0.1:5000/api/posts/<id>
PATCH http://127.0.0.1:5000/api/posts/37
