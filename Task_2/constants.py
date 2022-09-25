'''File for keeping literal strings used in main.py and app.py files'''

HOST = "localhost"
DB_NAME = "posts"
USERNAME = "root"
PASSWORD = "admin"

DB_URI = "mysql+pymysql://"
DB_URI += USERNAME
DB_URI += ":" + PASSWORD
DB_URI += "@" + HOST
DB_URI += "/" + DB_NAME

CREATED = "Post created successfully!"
UPDATED = "Post updated successfully!"

NOT_FOUND = "Post with the following ID is not in the database > "
ALL_REQUIRED = "All(Full_name, Picture_url, Date, Comment) fields required"
BAD_REQUEST = "Request model does not fit JSON format"
NOT_IMPLEMENTED = "This method is not implemented for the requested URL"
INTERNAL_SERVER_ERROR = "Internal server error"
REQUIREMENT1 = "Post must not be dated in the future"
REQUIREMENT2 = "Please provide both name and surname"

BASE_URL = "/api/posts/"
