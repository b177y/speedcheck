from flask import Flask, render_template, Response, request, redirect, url_for
from flask_bootstrap import Bootstrap
from sp.query import time_query
from sp.graph import plot
from forms import ConfigForm, CustomTime

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'you-will-never-guess' # CHANGE THIS !!!!!!!!!!!!!!!!

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = CustomTime()
    if request.method == 'POST':
        pass
    return redirect(url_for('show_graphs', timeframe="hour"))
    return render_template('index.html', form=form)

@app.route('/graphs/<timeframe>')
def show_graphs(timeframe):
    return render_template('graphs.html', timeframe=timeframe)

@app.route('/render/<gtime>/<gtype>')
def graph(gtime, gtype):
    results = time_query(gtime)
    imagedata = plot(results, gtype, gtime.capitalize())
    return Response(imagedata, mimetype="image/png")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = ConfigForm()
    if request.method == 'POST':
        form.update_db()
    form.load()
    return render_template("settings.html",title="Alert Config", form=form)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
