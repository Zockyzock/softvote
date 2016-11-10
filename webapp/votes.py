from flask_oauthlib.client import OAuth

from webapp import app

from flask import session, redirect, request, render_template
import httplib, json, sqlite3

from config import api, site, db, consumer_key, consumer_secret


oauth = OAuth()
faforever = oauth.remote_app('faforever',
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
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
            conn = httplib.HTTPSConnection(api)
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

        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("DELETE FROM votes WHERE vid=?",(vid,))
        c.execute("INSERT INTO votes VALUES(?,?)",(vid,candidate))
        conn.commit()
        
        return "Thanks for voting!"
    
    token = session.get("token")
    if not token:
        return redirect("/fail")

    return render_template("vote.html")


@app.route('/fail')
def fail():
    return "Something went wrong... :("

