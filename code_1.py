from flask import Flask, request, render_template

app = Flask(__name__)

def calculate_gpa(total_grades):
    total = 0
    for grade in total_grades:
        total += grade
    percentage = round((total / len(total_grades) + 1) * 20, 1)
    final_gpa = round(total / len(total_grades), 2)
    return final_gpa, percentage

@app.route('/', methods=['GET', 'POST'])
def calculate_score():
    if request.method == 'POST':
        try:
            grades = request.form.get('grades').split(' ')
            grades = [float(i) for i in grades]
            if not all(0 <= g <= 4 for g in grades):
                return render_template('error.html', error_message="Invalid grades. Please enter values between 0 and 4.")

            gpa = sum(grades) / len(grades)
 
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

            degree = request.form.get('degree').lower()
            if degree not in ["engineering", "medicine"]:
                return render_template('error.html', error_message="Invalid degree. Please enter 'engineering' or 'medicine'.")

            if degree == "engineering":
                final_score = gpa * 0.65 + math_qudurat * 0.2 + english_qudurat * 0.15
            elif degree == "medicine":
                final_score = gpa * 0.75 + math_qudurat * 0.15 + english_qudurat * 0.1

            return render_template('result.html', final_score=round(final_score, 1), gpa=round(gpa, 2))
        except ValueError:
            return render_template('error.html', error_message="Invalid input. Please check your values and try again.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)