from flask import Flask, request, make_response, render_template
import pickledb as dbms
import random as rand

# REST API PORTABILITY

null = None
false = False
true = True

# END PORTABILITY

app = Flask("communist-blog")

@app.route('/')
def index():
    return render_template("index.html")