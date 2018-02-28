"""Serve MonitorWare schema-compliant Syslog records from a RDBMS using a simple, fast web UI.
"""

# FIXME: there is a criminally ugly hack used below having to do with syslog tagging. I haven't gotten to the bottom
# of it yet, but it looks like python retains the ":" at the end of the tag...somehow. TBD.
#
# The below hacks hides the mess from the user.
#
# -- mburr@unintuitive.org

import psycopg2
import flask
import flask_wtf
import wtforms
import collections

app = flask.Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False  # we do not care

MAX_RECORDS_DEFAULT = 1000

columns = [
    ('id', ''),
    ('receivedat', 'Message received time'),
    ('priority', 'Priority'),
    ('fromhost', 'From host'),
    ('message', 'Log message'),
    ('syslogtag', 'Syslog tag'),
]

# we do this to preserve ordering.
default_columns = [n for n, _ in columns if n in ['fromhost', 'priority', 'receivedat', 'message']]

# we omit "id" since it is always displayed (as an anchor link)
display_columns = [(n,d) for n,d in columns if n != 'id']

priorities = [
    ('2', 'CRITICAL'),
    ('3', 'ERROR'),
    ('4', 'WARNING'),
    ('5', 'INFO'),
    ('6', 'DEBUG'),
]

class DBQueryForm(flask_wtf.FlaskForm):
    display_columns = wtforms.SelectMultipleField(id='display_columns',
                                                  label='Columns to display (multi-select):',
                                                  choices=display_columns,
                                                  default=default_columns,
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
        """Default method insists only on "POST". We use "GET".
        """
        return self.validate()


class Cell(object):
    """Represents a "cell" (<td />) in html. Attrs can be used for CSS selection.
    """
    def __init__(self, value, **kwargs):
        self.value = value
        self.__dict__.update(kwargs)


def get_treated_rows(columns, rows):
    """Brutally inefficient...

    Loop through the rows and make changes...
    """
    priorities_dict = dict(priorities)
    print priorities_dict
    new_rows = []
    for row in rows:
        new_row = []
        for column_name, value in zip(columns, row):
            if column_name == 'syslogtag':
                # FIXME: criminally ugly hack (see top of module)
                value = value[:-1]
            elif column_name == 'priority':
                value = priorities_dict[str(value)]
            # we use column_name as the <td/> "class"
            value = Cell(value, column_name=column_name)
            new_row.append(value)
        new_rows.append(new_row)

    return new_rows


def get_sql_query(data):
    query_template = """
        SELECT {display_columns} FROM systemevents WHERE priority <= '{priority}' AND syslogtag = '{syslogtag}';
    """
    data['display_columns'] = ', '.join(data['display_columns'])
    sql = query_template.format(**data)
    return sql

@app.route('/')
def index():
    args = flask.request.args
    form = DBQueryForm(args)

    # Populate defaults so we can have shorter URLs
    for name, attr in vars(DBQueryForm).items():
        if isinstance(attr, wtforms.core.UnboundField):
            if 'default' not in attr.kwargs:
                continue
            default = attr.kwargs['default']
            field = getattr(form, name)
            if not field.data:
                field.data = default

    rows = []
    column_headers = []
    if form.data['syslogtag'] is not None:

        # "id" is always in the columns we display, query for.
        if 'id' not in form.display_columns.data:
            form.display_columns.data.insert(0, 'id')

        # FIXME: criminally ugly hack (see top of module)
        form.syslogtag.data = form.data['syslogtag'] + u':'
        sql = get_sql_query(data=form.data)
        rows = get_rows(sql)

        c = dict(columns)
        for column_name in form.data['display_columns']:
            column_headers.append(c[column_name])
        rows = get_treated_rows(columns=form.data['display_columns'], rows=rows)
        # FIXME: criminally ugly hack (see top of module)
        form.syslogtag.data = form.data['syslogtag'][:-1]

    return flask.render_template('index.html', form=form, column_headers=column_headers, rows=rows)


def get_rows(sql):
    conn = psycopg2.connect("dbname='Syslog' user='logviewer' host='localhost' password='foo'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows



if __name__ == '__main__':
    app.run('0.0.0.0', port=1234, debug=True)

