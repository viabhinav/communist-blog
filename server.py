from flask import Flask, request, make_response, render_template, redirect
import pickledb as dbms
import random as rand
from werkzeug.exceptions import abort
from flaskext.markdown import Markdown as markdown
from html import unescape as unquote


def Reverse(tuples):
    new_tup = ()
    for k in reversed(tuples):
        new_tup = new_tup + (k,)
    return new_tup

# REST API PORTABILITY

null = None
false = False
true = True

# END PORTABILITY

# DATABASES CONFIG

postdb = dbms.load("posts.json", True)
#postdb.dcreate('posts')
app = Flask("communist-blog")
markdown(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/posts")
def viewposts():
    print(postdb.dgetall("posts"))
    print(tuple(postdb.dgetall("posts")))
    posts = [(k, v) for k, v in (postdb.dgetall("posts")).items()]
    return render_template("viewposts.html", posts=Reverse(posts))
    postdb.dump()

@app.route('/post/<string:postname>')
def viewpost(postname):
    try:
        post = postdb.dget("posts", postname)
        print(postdb.dget("posts", postname))
        return render_template("viewpost.html", content=unquote(post), heading=unquote(postname))
        postdb.dump()
    except:
        abort(404)

@app.route('/createpost')
def new_post():
    return render_template("createpost.html")
    postdb.dump()

@app.route('/editpost', methods=["GET"])
def edit_post():
    try:
        heading = request.args.get("heading")
        return render_template("editpost.html",heading=heading, content=unquote(str(postdb.dget("posts",heading)).strip().replace('\n', '\\n').replace('\r', '')))
        postdb.dump()
    except:
        return 'Failure'
@app.route('/newpost', methods=['GET'])
def newpost():
    try:
        postdb.dadd("posts", unquote(str(request.args.get('heading')), str(request.args.get('content'))))
        return redirect('/posts', code=302)
        postdb.dump()
    except Exception as e:
        print(e)
        abort(400)

@app.route('/edit-post', methods=['GET'])
def editpost():
    try:
        postdb.dpop("posts", unquote(request.args.get('oldheading')))
        postdb.dadd("posts", (str(request.args.get('heading')), str(unquote(request.args.get('content')))))
        return redirect('/post/'+str(request.args.get('heading')), code=302)
        postdb.dump()
    except KeyError as e:
        print(e)
        return str(e)

@app.route('/<string:post>/delete')
def deletepost(post):
    postdb.dpop("posts", post)
    return redirect('/posts')

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadx_file():
   if request.method == 'POST':
      f = request.files['file']
      mimetypes = ['video/3gpp','video/mp4','video/x-matroska','video/quicktime','video/x-flv','image/jpeg','image/bmp','image/svg+xml','image/png','image/tiff']
      if str(f.mimetype) in mimetypes: 
          f.save('static/'+(f.filename))
          return 'file uploaded successfully'
      else:
          return str(f.mimetype)+' not allowed'

app.run(host="0.0.0.0", port=1234)