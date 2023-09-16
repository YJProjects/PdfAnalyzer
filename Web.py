from Main import locate_response
from flask import Flask, render_template, request

app = Flask(__name__)

form_input = None

@app.route('/', methods=['GET', 'POST'])
def gfd():
    global form_input
    if request.method == 'POST':
        form_input = request.form.get("var")
    return render_template('index.html')

@app.after_request
def after_request(response):
    global form_input
    if form_input is not None:
        print(f"respone is : \n {locate_response(form_input)}")
    return response

if __name__ == '__main__':
    app.run(debug=True)
