from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def start():  # put application's code here
    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()
    print('hello!')
