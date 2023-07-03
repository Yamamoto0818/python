from flask import Flask, render_template, request,redirect,url_for, session
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k = 256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        # 通常のアクセスの場合
        return render_template('index.html')
    else:
        # register_exe() からredirect された場合
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if db.login(user_name, password):
        session['user'] = True 
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('top'))
    else :
        error = 'ログインに失敗しました。'
        input_data = {
            'user_name' : user_name,
            'password' : password
        }
        return render_template('index.html', error=error, data=input_data)

@app.route('/top', methods=['GET'])
def top():
    if 'user' in session:
        return render_template('top.html')
    else : 
        return redirect(url_for('index'))

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe',methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    # バリデーションチェック
    if user_name == '':
        error = 'ユーザ名が未入力です'
        return render_template('register.html', error=error)
    if password == '':
        error = 'パスワードが未入力です'
        return render_template('register.html', error=error)
    
    count = db.insert_user(user_name, password)
    
    if count  == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html',error =error)
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

#-----------------------------------------------------------

@app.route('/list')
def book_list():
    
    book_list = db.select_all_books()
    return render_template('book_list.html', books = book_list)

#--------------------------------------------------------------

@app.route('/registerbook')
def regi_book():
    return render_template('regibook.html')

@app.route('/registerbook_exe', methods=['POST'])
def regi_book_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    pages = request.form.get('pages')
    
    
    db.insert_book(title, author, publisher, pages)
    
    return render_template('regisucb.html')
    
@app.route('/editbook')
def edit_book():
    return render_template('editbook.html')  

@app.route('/delete_book')
def delete_book():
    return render_template('delete_book.html')

@app.route('/delete_book_exe', methods=['POST'])
def delete_book_exe():
    id = request.form.get('id')
    
    db.delete_book(id)
    
    return render_template('success_delete.html')

if __name__ == '__main__':
    app.run(debug=True)