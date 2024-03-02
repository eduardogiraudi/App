from flask import render_template, send_from_directory
from app import app


#route per la dist di react


@app.route('/')
@app.route('/login')
@app.route('/register')
@app.route('/forgot')
@app.route('/change_password')
@app.route('/activate_account')
@app.route('/get_verification_link')
@app.route('/response')
# @app.route('/<path:invalid_path>/')
def index():
    return render_template('/index.html')


@app.route("/manifest.json/")
def manifest():
    return send_from_directory('./login/build/', 'manifest.json')
