from flask import Flask, render_template, request, url_for, redirect
import json


app = Flask(__name__)


@app.route('/')
def index():
    """
    Displays the homepage by loading blog posts from the JSON file.

    This function loads blog posts from the 'data.json' file and renders the
    'index.html' template with the blog posts as context.

    Returns:
        A rendered HTML template for the homepage with the blog posts.
    """
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
    return render_template('index.html', post=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Adds a new blog post by handling GET and POST requests.

    This function handles the addition of a new blog post. It fetches the existing
    blog posts from the 'data.json' file, determines the highest existing ID, and
    assigns a new unique ID to the new post. The new post is then added to the list
    of blog posts and the updated list is saved back to the 'data.json' file.

    Returns:
        If the request method is GET, renders the 'add.html' template.
        If the request method is POST, redirects to the index page after adding the new post.
    """
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
    """
    Deletes a blog post by its ID.

    This function removes a blog post with the specified ID from the list of
    blog posts stored in the 'data.json' file and updates the file with the
    remaining posts. After deletion, it redirects to the index page.

    Args:
        post_id (int): The ID of the blog post to be deleted.

    Returns:
        A redirect to the index page after the post is deleted.
    """
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)

    blog_posts = [post for post in blog_posts if post.get('id') != post_id]

    with open('data.json', 'w') as f:
        json.dump(blog_posts, f, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Updates a blog post by its ID.

    This function fetches the existing blog posts from the 'data.json' file,
    finds the post with the specified ID, and updates its details based on
    the form data submitted via a POST request. The updated list of blog posts
    is then saved back to the 'data.json' file.

    Args:
        post_id (int): The ID of the blog post to be updated.

    Returns:
        If the request method is GET, renders the 'update.html' template with the post data.
        If the request method is POST, redirects to the index page after updating the post.
    """
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