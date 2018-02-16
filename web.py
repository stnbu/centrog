import psycopg2
import flask
import flask_wtf
import wtforms
import collections

app = flask.Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False  # we do not care

display_columns_choices = [
    ('foo', 'foo'),
    ('bar', 'bar'),
    ('baz', 'baz'),
]

class DBQueryForm(flask_wtf.FlaskForm):
    display_columns = wtforms.SelectMultipleField('display_columns', choices=display_columns_choices)
    sort_column = wtforms.TextField('sort_column')
    tag = wtforms.TextField('tag', validators=[wtforms.validators.InputRequired()])
    max_records = wtforms.IntegerField('max_records')

    def validate_on_submit(self):
        return self.validate()


@app.route('/')
def query():
    args = flask.request.args
    form = DBQueryForm(args)

    if form.validate_on_submit():
        print 'GOT'
    else:
        print 'DID NOT GOT'

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