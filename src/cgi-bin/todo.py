#!/usr/bin/env python
"""Todolist."""

import cgi
import html
import sqlite3

conn = sqlite3.connect('todolist.db')
curs = conn.cursor()

print('Content-type: text/html')
print('')


def print_html(data=''):
    """関数."""
    print('''\
    <!DOCTYPE html>
    <html>
    <read>
    <meta charset="UTF-8">
    <title>Todoリスト</title>
    </head>
    <body>
    <form action="todo.py" method="post">
    タスク名<input type="text" name="name">
    <input type="hidden" name="mode" value="add">
    <input type="submit" value="追加">
    </form>
    <ul>
    {0}
    </ul>
    </body>
    </html>
    '''.format(data))


form = cgi.FieldStorage()
mode = form.getvalue('mode')
# print(form)

if mode == 'add':
    name = form.getvalue('name')
    name = html.escape(name)

    sql = ('INSERT INTO tasks(name) VALUES(?)')
    curs.execute(sql, (name,))
    conn.commit()

if 'modify' in form:
    id = form.getvalue('id')
    id = html.escape(id)
    name = form.getvalue('upname')
    sql = ('UPDATE tasks SET name = ? WHERE id = ?')
    curs.execute(sql, (name, id,))
    conn.commit

if 'done' in form:
    id = form.getvalue('id')
    id = html.escape(id)

    sql = ('DELETE FROM tasks WHERE id = ?')
    curs.execute(sql, (id,))
    conn.commit()


curs.execute('SELECT * FROM tasks')
rows = curs.fetchall()

data = ""

for id, name in rows:
    data += '''
    <li>
    <form action="todo.py" method="post">
        <input type="text" value="{0}" name="upname">
        <input type="submit" value="済んだ" name="done">
        <input type="submit" value="更新する" name="modify" >
        <input type="hidden" name="id" value="{1}">
    </form>
    </li>
    '''.format(name, id)

print_html(data)
