from flask import Flask, request, render_template

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/public_tool', methods=['GET', 'POST'])
def public_tool():
    if request.method == 'POST':
        try:
            grades = request.form.get('grades').split(' ')
            grades = [float(i) for i in grades]
            if not all(0 <= g <= 100 for g in grades):
                return render_template('error.html', error_message="Invalid grades. Please enter values between 0 and 100.")

            if len(grades) != 3:
                return render_template('error.html', error_message="Please enter exactly three grades.")

            weights = [0.1, 0.2, 0.7]
            sum_grades = sum(g*w for g, w in zip(grades, weights))


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

            if degree == "engineering" and math_qudurat and english_qudurat:
                final_score = sum_grades * 0.65 + math_qudurat * 0.2 + english_qudurat * 0.15
            elif degree == "medicine" and math_qudurat and english_qudurat:
                final_score = sum_grades * 0.75 + math_qudurat * 0.15 + english_qudurat * 0.1
            else:
                final_score = sum_grades

            sum_grades = 'Your final percentage is: ' +  str(round(sum_grades, 1)) + '%'

            return render_template('result.html', final_score=round(final_score, 1), gpa=sum_grades)
        except ValueError:
            return render_template('error.html', error_message="Invalid input. Please check your values and try again.")

    return render_template('public_tool.html')

@app.route('/private_tool', methods=['GET', 'POST'])
def private_tool():
    if request.method == 'POST':
        try:
            grades = request.form.get('grades').split(' ')
            grades = [float(i) for i in grades]
            if not all(0 <= g <= 5 for g in grades):
                return render_template('error.html', error_message="Invalid grades. Please enter values between 0 and 5.")

            gpa = sum(grades) / len(grades) / 4 * 100

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


            if degree == "engineering" and math_qudurat and english_qudurat:
                gpa_on_4_point_scale = (gpa / 100) * 4
                final_score = gpa * 0.65 + math_qudurat * 0.2 + english_qudurat * 0.15
            elif degree == "medicine" and math_qudurat and english_qudurat:
                gpa_on_4_point_scale = (gpa / 100) * 4
                final_score = gpa * 0.75 + math_qudurat * 0.15 + english_qudurat * 0.1
            else:
                final_score = ((sum(grades) / len(grades)) + 1) * 20
                gpa_on_4_point_scale = (gpa / 100) * 4
            
            if final_score > 100:
                final_score = 100

            gpa = 'Your final high school GPA is: ' + str(round(gpa_on_4_point_scale, 2))

            return render_template('result.html', final_score=round(final_score, 1), gpa=gpa)
        except ValueError:
            return render_template('error.html', error_message="Invalid input. Please check your values and try again.")

    return render_template('private_tool.html')

if __name__ == '__main__':
    app.run(debug=True)