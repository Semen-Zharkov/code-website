from flask import Flask, render_template, url_for

Shad = Flask(__name__)

@Shad.route('/')
def index():
    return render_template('index.html')

@Shad.route('/request')
def test_page():
    return render_template('request.html')

@Shad.route('/about')
def about_page():
    return 'Здесь будет информация о нашем проекте'

if __name__ == '__main__':
    Shad.run(debug = True)
