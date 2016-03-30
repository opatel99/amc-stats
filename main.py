import ast
import os
import shelve
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)


@app.route('/', methods=['GET'])
def results():
    shelf = shelve.open('results.db', writeback=False)
    result = ast.literal_eval(str(shelf))
    shelf.close()
    return render_template('results.html', shelf=result)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('results'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if (request.form['user'] == 'user' and request.form['pass'] == 'pass'):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('admin'))
    if 'logged_in' in session:
        return render_template('admin.html')
    return render_template('login.html')


@app.route('/append', methods=['POST'])
def append():
    user = str(request.form['username'])
    shelf = shelve.open('results.db', writeback=True)
    if user not in shelf.keys():
        shelf[user] = {}
    if not request.form['amc10'] == '':
        shelf[user]['amc10'] = str("{0:.1f}"
                                   .format(float(request.form['amc10'])))
    if not request.form['amc12'] == '':
        shelf[user]['amc12'] = str("{0:.1f}"
                                   .format(float(request.form['amc12'])))
    if not request.form['aime'] == '':
        shelf[user]['aime'] = str(request.form['aime'])
    if 'amc10' in shelf[user] and 'aime' in shelf[user]:
        shelf[user]['index10'] = str("{0:.1f}"
                                     .format(float(shelf[user]['amc10']) +
                                             10 * float(shelf[user]['aime'])))
    if 'amc12' in shelf[user] and 'aime' in shelf[user]:
        shelf[user]['index12'] = str("{0:.1f}"
                                     .format(float(shelf[user]['amc12']) +
                                             10 * float(shelf[user]['aime'])))
    shelf.close()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()
