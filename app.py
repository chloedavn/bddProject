# app.py
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)
'''
db = psycopg2.connect(
    database="pccbdd",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)'''
#postgres://database_823a_user:ujd8HcDY1Qbg80u91CFOOUZMO3JwsWg2@dpg-ckp4nse2eoec739262mg-a.oregon-postgres.render.com/database_823a
db = psycopg2.connect(
    database="database_823a",
    user="database_823a_user",
    password="ujd8HcDY1Qbg80u91CFOOUZMO3JwsWg2",
    host="dpg-ckp4nse2eoec739262mg-a.oregon-postgres.render.com"
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM entities")
    entities = cursor.fetchall()
    return render_template('index.html', entities=entities)

@app.route('/create', methods=['POST'])
def create_entity():
    # Validate and process the input data
    # Add your data validation logic here

    name = request.form.get('name')
    age = int(request.form.get('age'))
    weight = float(request.form.get('weight'))
    is_student = 'is_student' in request.form
    with db.cursor() as cursor:
        insert_sql = """
        INSERT INTO entities (name, age, weight, is_student)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_sql, (name, age, weight, is_student))
        db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_entity(id):
    try:
        # Créez un curseur
        cursor = db.cursor()
        
        # Exécutez la requête DELETE avec l'ID spécifié
        cursor.execute("DELETE FROM entities WHERE id = %s", (id,))
        
        # Validez la suppression
        if cursor.rowcount > 0:
            db.commit()
        else:
            db.rollback()
        
        # Fermez le curseur
        cursor.close()
        
        # Redirigez l'utilisateur vers la page d'accueil ou une autre page appropriée
        return redirect(url_for('index'))
    except (Exception, psycopg2.DatabaseError) as error:
        # En cas d'erreur, gérez-la (par exemple, journalisez-la ou renvoyez une page d'erreur)
        return render_template('error.html', error=str(error))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_entity(id):
    try:
        # Créez un curseur
        cursor = db.cursor()

        if request.method == 'POST':
            # Si la requête est de type POST, cela signifie que l'utilisateur a soumis un formulaire de mise à jour.

            # Récupérez les nouvelles valeurs depuis le formulaire
            name = request.form.get('name')
            age = request.form.get('age')
            weight = request.form.get('weight')
            is_student = request.form.get('is_student') == 'on'

            # Exécutez la requête UPDATE pour mettre à jour l'entité avec les nouvelles valeurs
            cursor.execute("UPDATE entities SET name = %s, age = %s, weight = %s, is_student = %s WHERE id = %s",
                           (name, age, weight, is_student, id))

            # Validez la mise à jour
            db.commit()

            # Redirigez l'utilisateur vers la page d'accueil ou une autre page appropriée
            return redirect(url_for('index'))

        else:
            # Si la requête est de type GET, cela signifie que l'utilisateur souhaite afficher le formulaire de mise à jour.

            # Exécutez une requête SELECT pour récupérer les données actuelles de l'entité
            cursor.execute("SELECT * FROM entities WHERE id = %s", (id,))
            entity = cursor.fetchone()

            if entity:
                # Si l'entité existe, affichez le formulaire de mise à jour avec les valeurs actuelles
                return render_template('update.html', entity=entity)
            else:
                # Si l'entité n'existe pas, renvoyez l'utilisateur vers la page d'accueil ou une page d'erreur
                return redirect(url_for('index'))

    except (Exception, psycopg2.DatabaseError) as error:
        # En cas d'erreur, gérez-la (par exemple, journalisez-la ou renvoyez une page d'erreur)
        return render_template('error.html', error=str(error))

if __name__ == '__main__':
    app.run(debug=True)