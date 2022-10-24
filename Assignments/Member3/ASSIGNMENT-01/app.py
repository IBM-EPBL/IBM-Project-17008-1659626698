from flask import *;
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form["name"]
        email= request.form["email"]
        mobile = request.form["mobile"]
        return redirect(url_for('details', name=name, email=email, mobile=mobile))
    return render_template('index.html')


@app.route("/details", methods=['GET', 'POST'])
def details():
    name = request.form.get('name')
    email= request.form.get('email')
    mobile = request.form.get('mobile')
    return render_template('details.html', name=name, email=email, mobile=mobile)

if __name__ == "__main__":
    app.run(debug=True)