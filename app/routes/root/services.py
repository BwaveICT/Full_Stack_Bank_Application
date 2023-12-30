from app import app
from flask import render_template


@app.route('/services')
def services_page():
    return render_template('root/services.html')


