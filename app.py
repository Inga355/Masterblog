from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
    return render_template('index.html', post=blog_posts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)