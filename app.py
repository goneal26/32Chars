import hashlib
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect
# import random

app = Flask(__name__)


def generate_user_id():
    # Get the machine's hardware address (MAC address)
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])

    # You can add more randomization or hashing here if needed
    # For example, you can append a random string or hash the MAC address
    mac = hashlib.sha256(mac.encode('utf-8')).hexdigest()

    return mac


@app.route('/')
def create_post():  # put application's code here
    return render_template('newpost.html')


@app.route('/view_post')
def view_post():
    # Connect to the database
    conn = sqlite3.connect('identifier.sqlite')  # Update with your actual database name
    cursor = conn.cursor()

    # Get a random post from the 'posts' table
    cursor.execute('SELECT user_id, message FROM posts ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # If there are no posts in the database, set default values
    user_id = "No User"
    post = "No Post"

    # Update user_id and post if there is a result
    if result:
        user_id, post = result

    return render_template('viewpost.html', user_id=user_id, post=post)


@app.route('/submit_post', methods=['POST'])
def submit_post():
    message = request.form['post_content']
    user_id = generate_user_id()  # Replace with the actual user_id based on your authentication system

    # Connect to the database
    conn = sqlite3.connect('identifier.sqlite')
    cursor = conn.cursor()

    # Insert the new post into the 'posts' table
    cursor.execute('INSERT INTO posts (message, user_id) VALUES (?, ?)', (message, user_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return redirect('/view_post')  # Redirect to the home page or any other page after submitting the post


if __name__ == '__main__':
    app.run()
    print('hello!')
