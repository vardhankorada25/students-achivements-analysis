from flask import Flask,request,render_template

from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application=Flask(__name__)
app=application
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
     if request.method=='GET':
          return render_template('home.html')
     else:
            gender = request.form.get("gender") or "female"
            race_ethnicity = request.form.get("race_ethnicity") or "group A"
            parental_level_of_education = request.form.get("parental_level_of_education") or "some college"
            lunch = request.form.get("lunch") or "standard"
            test_preparation_course = request.form.get("test_preparation_course") or "none"
            reading_score = request.form.get("reading_score")
            writing_score = request.form.get("writing_score")
            if not reading_score or not writing_score:
                return render_template('home.html', error="Please provide reading and writing scores")
            data=CustomData(
                gender=gender,
                race_ethnicity=race_ethnicity,
                parental_level_of_education=parental_level_of_education,
                lunch=lunch,
                test_preparation_course=test_preparation_course,
                reading_score=float(reading_score),
                writing_score=float(writing_score), 
            )
            pred_df=data.get_data_as_data_frame()
            print("Dataframe--->",pred_df)
            predict_pipeline=PredictPipeline() 
            results=predict_pipeline.predict(pred_df)
            return render_template('home.html',results=results[0])
if __name__=="__main__":
     app.run(host='0.0.0.0',debug=True)

