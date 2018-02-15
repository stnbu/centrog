import psycopg2
import flask
import flask_wtf
import wtforms

app = flask.Flask(__name__)
app.secret_key = 'foo'


class DBQueryForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('name')


@app.route('/')
def query():
    form = DBQueryForm()
    # if form.validate_on_submit():
    #     return 'foo'
    name = flask.request.args.get('name')
    print 'you said', name
    return flask.render_template('index.html', form=form)


@app.route('/test')
def test():
    query = '''SELECT receivedat, priority, fromhost, message FROM systemevents WHERE priority = 3;'''
    conn = psycopg2.connect("dbname='Syslog' user='logviewer' host='localhost' password='foo'")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return str(len(rows))

if __name__ == '__main__':
    app.run('0.0.0.0', port=1234, debug=True)