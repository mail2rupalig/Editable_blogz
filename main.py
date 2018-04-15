from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    bodytext = db.Column(db.String(500))
    
   
    def __init__(self, title, bodytext):
        self.title = title
        self.bodytext = bodytext
        

@app.route('/newpost', methods=['POST','GET'])
def new_post():

    if request.method == 'POST':
        error_exists = False
        title_error = ""
        bodytext_error = ""
        title=request.form['title']
        bodytext=request.form['bodytext']
    
        if (not title) or (title.strip() == ""):
           title_error = "Please provide a title for the blog"
           error_exists=True
           

        if (not bodytext) or (bodytext.strip() == ""):
            bodytext_error = "Please provide blog text for the blog"
            error_exists = True
        
        if not error_exists :

            blog = Blog(title, bodytext)
            db.session.add(blog)
            db.session.commit()

            return redirect('/blog?id={0}'.format(blog.id))
        else:
            return render_template('newblog.html',title="Post New Blog",title_error=title_error,bodytext_error=bodytext_error,titlevalue=title,textarea=bodytext)  
    
    else:
        return render_template('newblog.html', title="Post New Blog")

        
@app.route('/blog', methods=['GET'])
def index():
  
    blogid = request.args.get('id')
    #print('blogid = ',blogid)
    if not blogid:
        posted_blogs = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('homepage.html', title="Build-A-Blog!", 
            posted_blogs = posted_blogs)
    
    else:
        id = int(blogid)
        print('id = ',id)
        posted_blog = Blog.query.get(id)
        return render_template('detailblog.html',title="Blog Detail",blog=posted_blog)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == '__main__':
    app.run()
app.run()