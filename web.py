import psycopg2
import flask

app = flask.Flask(__name__)
app.secret_key = ''

@app.route('/')
def index():
    if 'username' in flask.session:
        return 'Logged in as %s' % flask.escape(flask.session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        flask.session['username'] = flask.request.form['username']
        return flask.redirect(flask.url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/test')
def test():
    conn = psycopg2.connect("dbname='Syslog' user='logviewer' host='localhost' password='foo'")
    return '>'+str(conn)+'<'

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    flask.session.pop('username', None)
    return flask.redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=1234, debug=True)