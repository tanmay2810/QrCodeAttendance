from flask import Flask, render_template, request, jsonify
import qrCodeGenrator

# app = Flask(__name__)
app=Flask(__name__,template_folder='templates')
# model = pickle.load(open("cross_index.pkl","rb"))
urlpath = ''
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/admin')
def admin():
        return render_template('admin.html')
    # else:
    #     return render_template('home.html')



@app.route('/qrCode', methods=['POST'])
@app.route('/qrCode')
def results():
    qrCode = ''
    result = True
    if request.method == 'POST':
        urlpath = request.form['formUrl']
        print(urlpath)
        qrCodeGenrator.qrCodeGenrator(urlPath=urlpath)
        print(result)
        return render_template('qrCode.html',results=result)
    else:
        result = False
        return render_template('qrCode.html', results=result)




if __name__ == '__main__':
    app.run(debug=True)
