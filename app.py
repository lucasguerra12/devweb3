from flask import Flask , render_template,request,redirect
import mysql.connector
from config import DATABASE

app = Flask(__name__)

def db_connection():
    conn = mysql.connector.connect(
        host=DATABASE['host'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        database=DATABASE['database']
    )

    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contato',methods=['GET','POST'])
def contato():
    if request.method== 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']


        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contatos (nome,email,mensagem) VALUES (%s,%s,%s)",(nome,email,mensagem))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect ('/')
    
    return render_template('contato.html')

@app.route('/listar_contatos')
def listar_contatos():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contatos")
    contatos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('listar_contatos.html', contatos=contatos)

if __name__ == '__main__':
    app.run(debug=True)

    
