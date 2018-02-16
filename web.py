import psycopg2
import flask
import flask_wtf
import wtforms
import collections

app = flask.Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False  # we do not care

MAX_RECORDS_DEFAULT = 1000

columns = [
    ('id', 'Native database ordering'),
    ('priority', 'Priority'),
    ('syslogtag', 'Syslog tag'),
    ('message', 'Log message'),
    ('receivedat', 'Message received time'),
    ('fromhost', 'From host'),
]

priorities = [
    ('3', 'ERROR'),
    ('4', 'WARNING'),
]

class DBQueryForm(flask_wtf.FlaskForm):
    display_columns = wtforms.SelectMultipleField(id='display_columns',
                                                  label='Columns to display (multi-select):',
                                                  choices=columns,
                                                  default=['syslogtag', 'receivedat', 'message'],
                                                  validators=[wtforms.validators.InputRequired()])

    sort_column = wtforms.SelectField(id='sort_column',
                                      label='Column to sort by:',
                                      choices=columns,
                                      default='id')

    syslogtag = wtforms.TextField(id='syslogtag',
                            label='Syslog tag (required):',
                            validators=[wtforms.validators.InputRequired()])

    max_records = wtforms.IntegerField(id='max_records',
                                       label='Maximum records to return:',
                                       default=MAX_RECORDS_DEFAULT)

    priority = wtforms.SelectField(id='priority',
                                   label='Minimum message priority:',
                                   choices=priorities,
                                   default='3')

    def validate_on_submit(self):
        return self.validate()

def get_sql_query(data):
    query_template = """
        SELECT {display_columns} FROM systemevents WHERE priority = '{priority}' AND syslogtag = '{syslogtag}';
    """
    data['display_columns'] = ', '.join(data['display_columns'])
    sql = query_template.format(**data)
    return sql

@app.route('/')
def query():
    args = flask.request.args
    form = DBQueryForm(args)

    rows = []
    column_headers = []
    if form.validate_on_submit():
        sql = get_sql_query(data=form.data)
        rows = get_rows(sql)

        c = dict(columns)
        for column_name in form.data['display_columns']:
            column_headers.append(c[column_name])

    return flask.render_template('index.html', form=form, column_headers=column_headers, rows=rows)


def get_rows(sql):
    conn = psycopg2.connect("dbname='Syslog' user='logviewer' host='localhost' password='foo'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

if __name__ == '__main__':
    app.run('0.0.0.0', port=1234, debug=True)