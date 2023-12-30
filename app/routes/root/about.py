from app import app
from flask import render_template


@app.route('/about')
def about_page():
    return render_template('root/about.html')

