from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


app = Flask(__name__, static_folder='static')

def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'

app.config['SQLALCHEMY_BINDS'] = {
    'public': 'sqlite:///public_grades.db',
    'american': 'sqlite:///american_grades.db'
}

db = SQLAlchemy(app)

class AmericanGrade(db.Model):
    __bind_key__ = 'american'
    id = db.Column(db.Integer, primary_key=True)
    grade1 = db.Column(db.Float, nullable=False)
    grade2 = db.Column(db.Float, nullable=False)
    grade3 = db.Column(db.Float, nullable=False)
    grade4 = db.Column(db.Float, nullable=True)
    math_qudurat = db.Column(db.Float, nullable=True)
    english_qudurat = db.Column(db.Float, nullable=True)
    degree = db.Column(db.String(50), nullable=True)
    final_score = db.Column(db.Float, nullable=True)
    gpa = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(100), nullable=False)


class PublicGrade(db.Model):
    __bind_key__ = 'public'
    id = db.Column(db.Integer, primary_key=True)
    grade1 = db.Column(db.Float, nullable=False)
    grade2 = db.Column(db.Float, nullable=False)
    grade3 = db.Column(db.Float, nullable=False)
    math_qudurat = db.Column(db.Float, nullable=True)
    english_qudurat = db.Column(db.Float, nullable=True)
    degree = db.Column(db.String(50), nullable=True)
    final_score = db.Column(db.Float, nullable=True)
    gpa = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(100), nullable=False)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/public_tool', methods=['GET', 'POST'])
def public_tool():
    if request.method == 'POST':
        try:
            grade1 = float(request.form.get('grade1'))
            grade2 = float(request.form.get('grade2'))
            grade3 = float(request.form.get('grade3'))

            grades = [grade1, grade2, grade3]

            weights = [0.1, 0.2, 0.7]
            sum_grades = sum(g*w for g, w in zip(grades, weights))

            name = request.form.get('name')

            if not name:
                name = "Anonymous"

            math_qudurat = request.form.get('math_qudurat')
            if math_qudurat:
                math_qudurat = float(math_qudurat)
                if not 0 <= math_qudurat <= 100:
                    return render_template('error.html', error_message="Invalid Math Qudurat score. Please enter a value between 0 and 100.")

            english_qudurat = request.form.get('english_qudurat')
            if english_qudurat:
                english_qudurat = float(english_qudurat)
                if not 0 <= english_qudurat <= 100:
                    return render_template('error.html', error_message="Invalid English Qudurat score. Please enter a value between 0 and 100.")

            degree = request.form.get('degree')

            if not degree:
                return render_template('error.html', error_message="You need to select a degree.")
            
            degree = degree.lower()

            if degree == "engineering":
                if not math_qudurat:
                    return render_template('error.html', error_message="You need to input the Math Qudurat score for Engineering degree")
                if not english_qudurat:
                    return render_template('error.html', error_message="You need to input the English Qudurat score for Engineering degree")
                final_score = sum_grades * 0.65 + math_qudurat * 0.2 + english_qudurat * 0.15
            elif degree == "medicine":
                if not math_qudurat:
                    return render_template('error.html', error_message="You need to input the Math Qudurat score for Medicine degree")
                if not english_qudurat:
                    return render_template('error.html', error_message="You need to input the English Qudurat score for Medicine degree")
                final_score = sum_grades * 0.75 + math_qudurat * 0.15 + english_qudurat * 0.1
            else:
                final_score = sum_grades

            final_score = format_number(final_score)
            sum_grades = format_number(sum_grades)
            gpa = sum_grades
            sum_grades = 'Your final percentage is: ' +  str(round(sum_grades, 1)) + '%'

            final_score = format_number(final_score)

            public_grade = PublicGrade(
                name=name,
                grade1=grade1,
                grade2=grade2,
                grade3=grade3,
                math_qudurat=math_qudurat,
                english_qudurat=english_qudurat,
                degree=degree,
                final_score=final_score,
                gpa=gpa
            )

            db.session.add(public_grade)
            db.session.commit()
            
            return render_template('result.html', final_score=round(final_score, 1), gpa=sum_grades)
        except ValueError:
            return render_template('error.html', error_message="Invalid input. Please check your values and try again.")

    return render_template('public_tool.html')

@app.route('/private_tool', methods=['GET', 'POST'])
def private_tool():
    if request.method == 'POST':
        try:
            grade1 = float(request.form.get('grade1'))
            grade2 = float(request.form.get('grade2'))
            grade3 = float(request.form.get('grade3'))
            grade4 = float(request.form.get('grade4'))

            grades = [grade1, grade2, grade3, grade4]
            if not all(0 <= g <= 5 for g in grades):
                return render_template('error.html', error_message="Invalid grades. Please enter values between 0 and 5.")

            gpa = (sum(grades) / len(grades) + 1) * 20

            name = request.form.get('name')

            if not name:
                name = "Anonymous"

            
            math_qudurat = request.form.get('math_qudurat')
            if math_qudurat:
                math_qudurat = float(math_qudurat)
                if not 0 <= math_qudurat <= 100:
                    return render_template('error.html', error_message="Invalid Math Qudurat score. Please enter a value between 0 and 100.")

            english_qudurat = request.form.get('english_qudurat')
            if english_qudurat:
                english_qudurat = float(english_qudurat)
                if not 0 <= english_qudurat <= 100:
                    return render_template('error.html', error_message="Invalid English Qudurat score. Please enter a value between 0 and 100.")

            degree = request.form.get('degree')

            if not degree:
                final_score = gpa          
            degree = degree.lower()


            if degree == "engineering":
                if not math_qudurat:
                    return render_template('error.html', error_message="You need to input the Math Qudurat score for Engineering degree")
                if not english_qudurat:
                    return render_template('error.html', error_message="You need to input the English Qudurat score for Engineering degree")
                final_score = gpa * 0.65 + math_qudurat * 0.2 + english_qudurat * 0.15
            elif degree == "medicine":
                if not math_qudurat:
                    return render_template('error.html', error_message="You need to input the Math Qudurat score for Medicine degree")
                if not english_qudurat:
                    return render_template('error.html', error_message="You need to input the English Qudurat score for Medicine degree")
                final_score = gpa * 0.75 + math_qudurat * 0.15 + english_qudurat * 0.1
            else:
                final_score = gpa
            
            gpa_on_4_point_scale = (gpa / 20) - 1 
            
            if final_score > 100:
                final_score = 100

            final_score = format_number(final_score)

            gpa = 'Your final high school GPA is: ' + str(round(gpa_on_4_point_scale, 2))

            american_grade = AmericanGrade(
                name=name,
                grade1=grade1,
                grade2=grade2,
                grade3=grade3,
                grade4=grade4,
                math_qudurat=math_qudurat,
                english_qudurat=english_qudurat,
                degree=degree,
                final_score=final_score,
                gpa=gpa_on_4_point_scale
            )
            db.session.add(american_grade)
            db.session.commit()

            return render_template('result.html', final_score=round(final_score, 1), gpa=gpa)
        except ValueError:
            return render_template('error.html', error_message="Invalid input. Please check your values and try again.")

    return render_template('private_tool.html')

@app.route('/view_us_grades')
def view_us_grades():
    grades = AmericanGrade.query.all()
    return render_template('view_us_grades.html', grades=grades)

@app.route('/view_public_grades')
def view_public_grades():
    public_grades = PublicGrade.query.all()
    return render_template('view_public_grades.html', public_grades=public_grades)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)