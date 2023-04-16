from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = '127.0.0.1'
server.config["MYSQL_USER"] = 'auth_user'
server.config["MYSQL_PASSWORD"] = 'admin1234'
server.config["MYSQL_DB"] = 'auth'
# server.config["MYSQL_PORT"] = '3306'

@server.route("/login", methods=["POST"])
def login():

    # check db for username and password
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT email, password FROM user WHERE email=%s", ('ivan@scrobot.net',)
    )
    
    if cur.rowcount > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = 'admin1234'

        if 'ivan@scrobot.net' != email or 'admin1234' != password:
            return "invalid credentials", 401
        else:
            return "Hurray", 200
    else:
        return "invalide credentials", 401
    
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=9090)