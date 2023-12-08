import hashlib
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect, session
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__)

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()


# Function to clear the database
def clear_database():
    conn = sqlite3.connect('identifier.sqlite')
    cursor = conn.cursor()

    # Clear the 'posts' table
    cursor.execute('TRUNCATE TABLE posts')  # could also use truncate table

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Schedule the task to run daily at midnight UTC using cron trigger
scheduler.add_job(clear_database, trigger=CronTrigger(hour=0, minute=0, second=0, timezone='UTC'))


# this works well enough for a unique user id function for now
def generate_user_id():
    # Get the machine's hardware address (MAC address)
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
    mac = hashlib.sha256(mac.encode('utf-8')).hexdigest()
    out_string = ""
    for item in random.sample(mac, 8):
        out_string = out_string + item

    return out_string


@app.route('/')
def create_post():  # put application's code here
    return render_template('newpost.html')


@app.route('/view_post')
def view_post():
    # Connect to the database
    conn = sqlite3.connect('identifier.sqlite')
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
    user_id = 'user_' + generate_user_id()  # Replace with the actual user_id based on your authentication system

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
