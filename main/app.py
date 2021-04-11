from flask import Flask, make_response, request, url_for, redirect, session
app = Flask(__name__)

app.secret_key = "sfdasdfa"

@app.route('/login/<name>')
def login(name):
    session['login_in'] = True
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response
    
    

@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = f'hello {name}'
        if 'login_in' in session:
            response += '[Auth]'
        else:
            response += '[UnAuth]'
    return response


@app.route('/logout')
def logout():
    if 'login_in' in session:
        session.pop('login_in')
    return redirect(url_for('hello'))

