from flask_oauthlib.client import OAuth
from webapp import app
from flask import session, redirect, request, render_template
import http, json, pymysql, os

site = os.environ['SITE']
api = os.environ['API']
db_creds = {
    'password': os.environ['MYSQL_ROOT_PASSWORD'],
    'db': os.environ['MYSQL_DATABASE'],
    'host': os.environ['MYSQL_HOSTNAME'],
    'user': os.environ['MYSQL_USER']
}
oauth = OAuth()
faforever = oauth.remote_app('faforever',
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    base_url=api+"/oauth/authorize",
    access_token_url=api+"/oauth/token",
    request_token_params={"scope":"public_profile"}
)

@app.route("/")
def root():
    return render_template("home.html")

@app.route("/login")
def login():
    return faforever.authorize(callback=site+"/oauth")


@app.route('/oauth',methods=["GET","POST"])
@faforever.authorized_handler
def test3(resp):
    if resp is None:
        return redirect("/fail")
    token = resp["access_token"]
    session['token'] = token

    return redirect("/vote")

@app.route('/vote',methods=["GET","POST"])
def vote():
    if request.method == "POST":
        token = session.get("token")
        if not token:
            return redirect("/fail")
        try:
            conn = http.client.HTTPSConnection(api)
            headers = {"Authorization":"Bearer " + token}
            conn.request("GET","/players/me",headers=headers)
            response = conn.getresponse()
            data = response.read()
            vid = json.loads(data)["data"]["id"]
        except Exception as e:
            print(e)
            return redirect("/fail")

        candidate = request.form.get("candidate")
        if not candidate:
            return redirect("/fail")

        conn = pymysql.connect(**db_creds)
        with conn as cursor:
            cursor.execute("DELETE FROM votes WHERE vid=?",(vid,))
            cursor.execute("INSERT INTO votes VALUES(?,?)",(vid,candidate))
        conn.commit()

        return "Thanks for voting!"

    token = session.get("token")
    if not token:
        return redirect("/fail")

    return render_template("vote.html")


@app.route('/fail')
def fail():
    return "Something went wrong... :("
