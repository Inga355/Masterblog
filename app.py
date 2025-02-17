from flask import Flask, render_template, request, url_for, redirect
import json


app = Flask(__name__)


def fetch_post_by_id(post_id):
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
        fetch_post = next((post for post in blog_posts if post.get('id') == post_id), None)
        return fetch_post


@app.route('/')
def index():
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
    return render_template('index.html', post=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
        highest_id = 0
        for post in blog_posts:
            if 'id' in post and post.get('id') > highest_id:
                highest_id = post.get('id')
        if request.method == 'POST':
            new_author = request.form['author']
            new_title = request.form['title']
            new_content = request.form['content']
            new_post = {
                'id': highest_id + 1,
                'author': new_author,
                'title': new_title,
                'content': new_content
            }
            blog_posts.append(new_post)
            with open('data.json', 'w') as f:
                json.dump(blog_posts, f, indent=4)
            return redirect(url_for('index'))
        return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
    blog_posts = [post for post in blog_posts if post.get('id') != post_id]
    with open('data.json', 'w') as f:
        json.dump(blog_posts, f, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
        post = next((post for post in blog_posts if post.get('id') == post_id), None)
        if request.method == 'POST':
            blog_posts = [post for post in blog_posts if post.get('id') != post_id]
            new_author = request.form['author']
            new_title = request.form['title']
            new_content = request.form['content']
            new_post = {
                'id': post_id,
                'author': new_author,
                'title': new_title,
                'content': new_content
            }
            blog_posts.append(new_post)
            with open('data.json', 'w') as f:
                json.dump(blog_posts, f, indent=4)
            return redirect(url_for('index'))
        return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)