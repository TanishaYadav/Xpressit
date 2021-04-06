from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(30), nullable = False , default = 'N/A')
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False , default = datetime.utcnow() )

    def __repr__(self):
        return f'Blog post {self.id}'



# all_posts = [
#     {
#         'title' : 'Mera post great',
#         'content' : 'LA la la la ..... ',
#         'author' : 'Tani'
#     },
#
#     {
#         'title' : 'Mujhse smart kaun !',
#         'content' : 'This is so annoying Stupid Bahubali !'
#     }
#             ]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods  = ['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts = all_posts)

# @app.route('/home')
# def intro():
#     return "Doing really well ! Go on"

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/new', methods = ['POST','GET'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new.html')

@app.route('/login')
def login():
    return "Login Here"

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts/edit/<int:id>',methods = ['POST','GET'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)


# @app.route('/person/<string:user_name>')
# def person(user_name):
#     return f'Hello {user_name}! Welcome'
#
# @app.route('/home/user/<string:name>/posts<int:user_id>')
# def welcome(name,user_id):
#     return f'Hello {name}! Welcome your id {user_id}'
#
# @app.route('/onlyget', methods = ['GET'])
# def get_req():
#     return 'You can only get this page'



if __name__ == '__main__':
    app.run(debug = True)