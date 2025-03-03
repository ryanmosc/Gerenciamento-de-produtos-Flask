import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash
import bcrypt
import re
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
from flask import make_response
import io




app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sua senha',
        database='Seu banco de dados'
    )
    

class Usuario(UserMixin):
    def __init__(self, id):
        self.id = id
        self.nome = id  



@login_manager.user_loader
def load_user(user_id):
    return Usuario(user_id)



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome'].strip()
        senha = request.form['senha']
        
        
        if not nome_usuario or not senha:
            flash('Nome e senha não podem estar vazios!', 'error')
            return render_template('login.html')
        
        
        conexao = get_db_connection()
        cursor = conexao.cursor()
        
        
        cursor.execute('SELECT nomes, senhas FROM usuarios WHERE nomes = %s', (nome_usuario,))
        resultado = cursor.fetchone()
        
        if not resultado:
            flash('Acesso negado! Usuário ou senha inválidos.', 'error')
            cursor.close()
            conexao.close()
            return render_template('login.html')
        
        _, hash_armazenado = resultado  
        senha_bytes = senha.encode('utf-8')  
        
        
      
        if isinstance(hash_armazenado, str):
            hash_armazenado = hash_armazenado.encode('utf-8')
        
        
        if bcrypt.checkpw(senha_bytes, hash_armazenado):
            user = Usuario(nome_usuario)  
            login_user(user)
            flash('Acesso liberado!', 'success')
            cursor.close()
            conexao.close()
            return redirect(url_for('home'))
        else:
            flash('Acesso negado! Usuário ou senha inválidos.','error')
            cursor.close()
            conexao.close()
            return render_template('login.html')
    
    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email']
        senha = request.form['senha']
        
        if not nome:
            flash('O nome não pode estar vazio!', 'error')
            return render_template('registro.html')
        
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            flash('Email inválido! Use um formato válido (ex.: usuario@dominio.com)', 'error')
            return render_template('registro.html')
        
        if len(senha) < 8:
            flash('Senha muito curta (mínimo 8 caracteres)!', 'error')
            return render_template('registro.html')
        
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE enails = %s', (email,))
        if cursor.fetchall():
            flash('Email já cadastrado!', 'error')
            cursor.close()
            conexao.close()
            return render_template('registro.html')
        
        senha_bytes = senha.encode('utf-8')  
        salt = bcrypt.gensalt()  
        hash_senha = bcrypt.hashpw(senha_bytes, salt)  
        cursor.execute('INSERT INTO usuarios (nomes, enails, senhas) VALUES (%s, %s, %s)', (nome, email, hash_senha))
        conexao.commit()
        cursor.close()
        conexao.close()
        flash('Usuário cadastrado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')



@app.route('/home')
@login_required
def home():
    return render_template('home.html')



@app.route('/criar', methods=['GET', 'POST'])
@login_required
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        try:
            quantidade = int(request.form['quantidade'])
            valor = float(request.form['valor'])
            conexao = get_db_connection()
            cursor = conexao.cursor()
            cursor.execute('INSERT INTO vendas (nome_produto,quantidade, valor) VALUES (%s, %s,%s)', (nome, quantidade, valor))
            conexao.commit()
            cursor.close()
            conexao.close()
            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('criar'))
        except ValueError:
            flash('Erro: Insira um valor numérico válido!', 'error')
    return render_template('criar.html')



@app.route('/listar')
@login_required
def listar():
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM vendas')
        produtos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return render_template('listar.html', produtos=produtos)
    except mysql.connector.Error as e:
        flash(f'Erro ao listar produtos: {e}', 'error')
        return redirect(url_for('home'))



@app.route('/atualizar', methods=['GET', 'POST'])
@login_required
def atualizar():
    conexao = get_db_connection()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM vendas')
    produtos = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            id_update = int(request.form['id'])
            if not id_update:
                flash('O ID do produto não pode ser vazio!', 'error')
                cursor.close()
                conexao.close()
                return render_template('atualizar.html', produtos=produtos)
            
            cursor.execute('SELECT * FROM vendas WHERE idVendas = %s', (id_update,))
            resultado = cursor.fetchone()
            if not resultado:
                flash('Nenhum produto encontrado com esse ID!', 'error')
                cursor.close()
                conexao.close()
                return render_template('atualizar.html', produtos=produtos)
            
            nome = request.form['nome'].strip()
            if not nome:
                flash('O nome do produto não pode estar vazio!', 'error')
                cursor.close()
                conexao.close()
                return render_template('atualizar.html', produtos=produtos)
            
            quantidade = int(request.form['quantidade'])
            if quantidade < 0:
                flash('A quantidade de produtos deve ser maior ou igual a 0!', 'error')
                cursor.close()
                conexao.close()
                return render_template('atualizar.html', produtos=produtos)
            
            valor = float(request.form['valor'])
            if valor < 0:
                flash('O valor do produto deve ser maior ou igual a 0!', 'error')
                cursor.close()
                conexao.close()
                return render_template('atualizar.html', produtos=produtos)
            
            vendas = int(request.form['vendas'])
            if vendas < 0:
                flash('As vendas de produtos devem ser maior ou igual a 0!', 'error')
                cursor.close()
                conexao.close()
                return render_template('atualizar.html', produtos=produtos)
            
            cursor.execute('UPDATE vendas SET nome_produto = %s, quantidade = %s, valor = %s, vendas = %s WHERE idVendas = %s', (nome, quantidade, valor, vendas, id_update))
            if cursor.rowcount == 0:
                flash('Nenhum produto encontrado com esse ID!', 'error')
            else:
                conexao.commit()
                flash('Produto atualizado com sucesso!', 'success')
            cursor.close()
            conexao.close()
            return redirect(url_for('atualizar'))
        
        except ValueError as ve:
            flash('Erro: O ID deve ser um número inteiro ou o valor deve ser numérico válido!', 'error')
            cursor.close()
            conexao.close()
            return render_template('atualizar.html', produtos=produtos)
        except mysql.connector.Error as e:
            flash(f'Erro no banco de dados: {e}', 'error')
            conexao.rollback()
            cursor.close()
            conexao.close()
            return render_template('atualizar.html', produtos=produtos)
        
        
    
    cursor.close()
    conexao.close()
    return render_template('atualizar.html', produtos=produtos)



@app.route('/deletar', methods=['GET', 'POST'])
@login_required
def deletar():
    if request.method == 'POST':
        try:
            id_produto = int(request.form['id'])
            conexao = get_db_connection()
            cursor = conexao.cursor()
            cursor.execute('SELECT * FROM vendas WHERE idVendas = %s ', (id_produto,))
            resultado = cursor.fetchone()
            if resultado is None:
                flash('Erro: Id não encontrado ou inexistente', 'error')
                return render_template('deletar.html')
            else:
                cursor.execute('DELETE FROM vendas WHERE idVendas = %s', (id_produto,))
                flash('Produto removido com sucesso!', 'success')
                conexao.commit()
                
            
            cursor.close()
            conexao.close()
            
            return redirect(url_for('deletar'))
        except ValueError:
            flash('Erro: Insira um ID válido!', 'error')
    return render_template('deletar.html')


@app.route('/relatorios', methods=['GET', 'POST'])
@login_required
def relatorios():
    try:
        conexao = get_db_connection()
      
        query = "SELECT idVendas, nome_produto, quantidade, valor, Vendas FROM vendas"
        df = pd.read_sql(query, conexao)
        conexao.close()

        
        if df.empty:
            flash('Nenhum dado de vendas encontrado!', 'error')
            return render_template('relatorios.html')

        # Cálculos com Pandas
        df['total_por_produto'] = df['Vendas'] * df['valor']  
        media_valor = df['valor'].mean()  
        total_vendas_geral = df['total_por_produto'].sum()  
        produto_mais_vendido = df.loc[df['Vendas'].idxmax()]['nome_produto'] 
        produto_menos_vendido = df.loc[df['Vendas'].idxmin()]['nome_produto']  

  
        produto_especifico = None
        if request.method == 'POST':
            id_produto = request.form.get('id_produto')
            if id_produto:
                try:
                    id_produto = int(id_produto)
                    produto_especifico = df[df['idVendas'] == id_produto].to_dict('records')
                    if not produto_especifico:
                        flash('Produto não encontrado!', 'error')
                    else:
                        produto_especifico = produto_especifico[0]
                except ValueError:
                    flash('ID inválido! Insira um número inteiro.', 'error')

        
        tabela_html = df.to_html(index=False, classes='table table-striped')

        return render_template(
            'relatorios.html',
            tabela=tabela_html,
            media_valor=media_valor,
            total_vendas_geral=total_vendas_geral,
            produto_mais_vendido=produto_mais_vendido,
            produto_menos_vendido=produto_menos_vendido,
            produto_especifico=produto_especifico
        )
    except Exception as e:
        flash(f'Erro ao gerar relatórios: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/exportar_relatorio')
@login_required
def exportar_relatorio():
    try:
        conexao = get_db_connection()
        query = "SELECT idVendas, nome_produto, quantidade, valor, Vendas FROM vendas"
        df = pd.read_sql(query, conexao)
        conexao.close()

        if df.empty:
            flash('Nenhum dado para exportar!', 'error')
            return redirect(url_for('relatorios'))

       
        df['total_por_produto'] = df['Vendas'] * df['valor']


        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, sep=';', encoding='utf-8-sig') 
        csv_data = csv_buffer.getvalue()
        csv_buffer.close()

        response = make_response(csv_data)
        response.headers['Content-Disposition'] = 'attachment; filename=relatorio_vendas.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response
    except Exception as e:
        flash(f'Erro ao exportar relatório: {e}', 'error')
        return redirect(url_for('relatorios'))
@app.route('/logout')
@login_required  
def logout():
    try:
        logout_user()  
        flash('Você foi desconectado com sucesso!', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash('Ocorreu um erro ao tentar sair. Tente novamente mais tarde.', 'error') 
        return redirect(url_for('home')) 
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
