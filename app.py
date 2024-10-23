from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

def calculate_last_third_of_night(maghrib_time, fajr_time):
    # تحويل الأوقات إلى كائنات وقت
    maghrib = datetime.strptime(maghrib_time, "%H:%M")
    fajr = datetime.strptime(fajr_time, "%H:%M")
    
    # إذا كان الفجر بعد منتصف الليل، نضيف يومًا كاملًا لتسهيل الحساب
    if fajr < maghrib:
        fajr += timedelta(days=1)
    
    # حساب مدة الليل
    night_duration = fajr - maghrib
    
    # حساب مدة الثلث
    third_duration = night_duration / 3
    
    # حساب بداية الثلث الأخير
    last_third_start = fajr - third_duration
    
    return last_third_start.time()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        maghrib_time = request.form.get("maghrib_time")
        fajr_time = request.form.get("fajr_time")
        try:
            last_third_start = calculate_last_third_of_night(maghrib_time, fajr_time)
            return render_template("index.html", result=last_third_start, maghrib_time=maghrib_time, fajr_time=fajr_time)
        except ValueError:
            return render_template("index.html", error="تأكد من إدخال الأوقات بشكل صحيح باستخدام تنسيق 24 ساعة (HH:MM)")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
