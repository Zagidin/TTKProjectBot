from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base.config import Client, Base

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Замените на свой секретный ключ

# Настройка базы данных
engine = create_engine("sqlite:///keywords.db")  # Укажите вашу базу данных
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route('/table', methods=['GET', 'POST'])
def show_table():
    session = Session()

    if request.method == 'POST':
        # Добавление нового намерения
        service = request.form['service']
        intent = request.form['intent']
        phone = request.form['phone']
        description = request.form['description']

        new_intent = Client(service=service, intent=intent, phone=phone, description=description)
        session.add(new_intent)
        session.commit()
        return redirect(url_for('show_table'))

    clients = session.query(Client).all()  # Получение всех записей из таблицы KeywordIntent
    return render_template('table.html', clients=clients)  # Передача данных в шаблон


@app.route('/delete/<int:id>', methods=['POST'])
def delete_intent(id):
    session = Session()
    intent_to_delete = session.query(Client).filter_by(id=id).first()
    if intent_to_delete:
        session.delete(intent_to_delete)
        session.commit()
    return redirect(url_for('show_table'))


if __name__ == "__main__":
    app.run(debug=True)