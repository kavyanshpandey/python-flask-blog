from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    Author = db.Column(db.String(20), nullable=False, default='Unknown')
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


all_posts = [
    {
        'title': 'Post1',
        'Content': 'This is the content of post 1',
        'Author': 'Kavyansh Pandey'
    },
    {
        'title': 'Post2',
        'Content': 'This is the content of post 2',
        # 'Author': ''
    }
]


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/aboutus', methods=['GET'])
def aboutpage():
    return render_template('about.html')


@app.route('/contactus', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/posts/newposts', methods=['GET', 'POST'])
def addPosts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['Content']
        post_author = request.form['Author']

        if post_author == '':
            post_author = 'Unknown'

        new_post = BlogPost(
            title=post_title, Content=post_content, Author=post_author)

        db.session.add(new_post)

        db.session.commit()

        return redirect('/posts')

    else:
        return render_template('add_posts.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':

        post_title = request.form['title']
        post_content = request.form['Content']
        post_author = request.form['Author']

        if post_author == '':
            post_author = 'Unknown'

        new_post = BlogPost(
            title=post_title, Content=post_content, Author=post_author)

        db.session.add(new_post)

        db.session.commit()

        return redirect('/posts')

    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
def deletePost(id):
    post_id = BlogPost.query.get(id)
    db.session.delete(post_id)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def editPost(id):
    post_id = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post_id.title = request.form['title']
        post_id.Content = request.form['Content']
        post_id.Author = request.form['Author']

        db.session.commit()

        return redirect('/posts')

    else:
        return render_template('edit.html', post=post_id)

# Main function
if __name__ == "__main__":
    PORT = 5000
    app.run(debug=True, port=PORT)
