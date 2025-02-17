from flask import Flask, render_template, request, url_for, redirect
import json


app = Flask(__name__)


@app.route('/')
def index():
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
    return render_template('index.html', post=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
        if request.method == 'POST':
            print(f'erster Post : {blog_posts}')
            new_author = request.form['author']
            new_title = request.form['title']
            new_content = request.form['content']
            new_post = {
                'author': new_author,
                'title': new_title,
                'content': new_content
            }
            blog_posts.append(new_post)
            print(blog_posts)
            with open('data.json', 'w') as f:
                json.dump(blog_posts, f, indent=4)
            return redirect(url_for('index'))
        return render_template('add.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)