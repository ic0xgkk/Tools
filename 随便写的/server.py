import flask
import sqlite3
import markdown


def md_conv(src: str):
    html = (markdown.markdown(src, extensions=[
        'fenced_code',
        'toc',
        'tables',
        'sane_lists'
    ]))
    return html


class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect("database.sqlite", check_same_thread=False)
        self.init()

    def __del__(self):
        self.conn.close()

    def init(self):
        sql = """
CREATE TABLE IF NOT EXISTS UserInfo(
    userid INTEGER PRIMARY KEY AUTOINCREMENT ,
    cardid VARCHAR(50),
    username VARCHAR(20),
    phone VARCHAR(20),
    other VARCHAR(20),
    gentime TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
)
"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            self.conn.rollback()
            cursor.close()
            raise Exception("数据库初始化失败:" + str(e))

    def insert_user(self, cardid: str, username: str, phone: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM UserInfo WHERE cardid='%s'" % cardid)
        data = cursor.fetchall()
        try:
            if len(data) == 0:
                cursor.execute("INSERT INTO UserInfo(cardid, username, phone) VALUES('%s', '%s', '%s')" %
                               (cardid, username, phone))
            else:
                cursor.execute("UPDATE UserInfo SET username='%s', phone='%s' WHERE cardid='%s'" %
                               (str(username), str(phone), str(cardid)))

            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            self.conn.rollback()
            cursor.close()
            raise Exception("插入用户失败:" + str(e))
        return "操作成功"

    def search(self, cardid: str):
        if cardid == "请输入查询ID":
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Userinfo")
            search_result = "| 序号 | Card ID | 用户名称 | 手机号码 | 备注 | 最近时间 |\n" \
                            "| ------ | ------ | ------ | ------ | ------ | ------ |\n"
            result = cursor.fetchall()
            cursor.close()
            for row in result:
                search_result += str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]) + \
                                " | " + str(row[4]) + " | " + str(row[5]) + "\n"
            return md_conv(search_result)
        else:
            cursor =  self.conn.cursor()
            cursor.execute("SELECT * FROM UserInfo WHERE cardid='%s'" % str(cardid)) # 建议使用SQL参数化查询，防注入
            result = cursor.fetchall()
            if result is None:
                cursor.close()
                return "查无CARD ID=" + cardid + "的记录"
            else:
                search_result = "| 序号 | Card ID | 用户名称 | 手机号码 | 最近时间 |\n" \
                                "| ------ | ------ | ------ | ------ | ------ |\n"
                result = cursor.fetchall()
                cursor.close()
                for row in result:

                    search_result += str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]) \
                                    + " | " + str(row[5]) + "\n"
                return md_conv(search_result)


class FlaskApp(object):
    host = "0.0.0.0"
    port = 9001
    debug = True
    table = """
<html>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/css/materialize.min.css">
	<head>		
		<title>用户信息平台</title>
	</head>
	<body>
	<div class="container">
		<div class="green-text text-darken-2">
			<h3>信息如下</h3>
			<div class="valign-wrapper">
				<h5 class="valign">
					%s
				</h5>
			</div>
		</div>
    </div>
	</body>
</html>
    """

    def __init__(self, db: Database):
        self.app = flask.Flask(__name__)
        self.url_route()
        self.db = db

    def start(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug, threaded=False)

    def url_route(self):
        self.app.add_url_rule('/register', 'register', self.register, methods=['GET'])
        self.app.add_url_rule('/search', 'search', self.search, methods=['GET'])

    def register(self):
        cardid = flask.request.args.get('cardid')
        username = flask.request.args.get('username')
        phone = flask.request.args.get('phone')
        if cardid is None or \
            username is None or \
                phone is None:
            return "拒绝访问"
        html = self.db.insert_user(cardid, username, phone)
        return html

    def search(self):
        cardid = flask.request.args.get('cardid')

        if cardid is None:
            return "拒绝访问"
        html = self.db.search(cardid)
        data = html.replace('<table>', '<table class="striped">')
        return self.table % data

if __name__ == '__main__':
    db = Database()
    f = FlaskApp(db)
    f.start()