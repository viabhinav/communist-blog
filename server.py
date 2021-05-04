from flask import Flask, request, make_response, render_template
import pickledb as dbms
import random as rand
from werkzeug.exceptions import abort

# REST API PORTABILITY

null = None
false = False
true = True

# END PORTABILITY

# DATABASES CONFIG

postdb = dbms.load("posts.json", True)
postdb.dcreate("posts")
postdb.dadd("posts", ("How to be a communist", 'The proletariat is the working-class; people who provide work to an employer in exchange for wages, but do not have any ownership of the company they work for or the "means of production," meaning the land, tools, factories, office buildings, raw materials, etc. that make their work possible. Most members of the proletariat have little control or say over their own labor, and do not share in the profits of their employer.[2]\nBecause the proletariat have no control over their labor and are dependent on wages to survive, they are easily exploited by their employers.\nThe oppressors of the proletariat are called the "bourgeoisie" in Marxist terms, the wealthy capitalists who own the corporations, factories, and land, and consequently, most of the worlds wealth.[3]\nThe modern concept of the 99% is very similar to Karl Marxs concept of the proletariat, and the 1% is analogous to the bourgeoisie.\nA key tenet of communism is that the proletariat should strive to gain control over the means of production, and own and manage it collectively.'))
postdb.dadd("posts", ("How to be killed by TMC goons in WB!", "The art of being killed by goons, is very subtle, and involves joining a political party, which is the opposing party of the TMC. The exact process of doing this is to join BJP just before elections, and going to face a leader, and win. But do this ensuring TMC gets the government. Mission Accomplished!"))
app = Flask("communist-blog")

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/posts")
def viewposts():
    print(postdb.dgetall("posts"))
    print(tuple(postdb.dgetall("posts")))
    posts = [(k, v) for k, v in (postdb.dgetall("posts")).items()]
    return render_template("viewposts.html", posts=posts)

@app.route('/post/<string:postname>')
def viewpost(postname):
    try:
        post = postdb.dget("posts", postname)
        print(postdb.dget("posts", postname))
        return render_template("viewpost.html", content=post, heading=postname)
    except Exception as e:
        abort(404)

@app.route('/createpost')
def new_post():
    return render_template("createpost.html")

@app.route('/newpost', methods=['GET'])
def newpost():
    try:
        postdb.dadd("posts", (str(request.args.get('heading')), str(request.args.get('content'))))
        return render_template('viewposts.html')
    except:
        abort(404)

app.run(host="0.0.0.0", port=1234)