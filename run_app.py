import os
import webapp
from webapp import app

#change this
context = ("ssl/example.crt","ssl/example.key")

os.environ['DEBUG'] = '1'

#change this too
app.secret_key = 'test-key'

app.config['SESSION_TYPE'] = 'filesystem'

app.run(host="softvote.cloudapp.net",port = 443,debug=False,ssl_context=context)
