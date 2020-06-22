import matplotlib.pyplot as plt
import json

with open("freeudemy.json", "r", encoding="utf-8") as file:
    data = json.load(file)

course_points = data["udemycoupons"]
all_points = []

bad_points = []
mid_points = []
good_points = []
well_points = []
for i in course_points:
    all_points.append(float(i['Course Point']))

while all_points:
    if all_points[0] == 0.0 or all_points[0] <= 2.5:
        bad_points.append(all_points[0])
    elif all_points[0] == 2.6 or all_points[0] <= 3.4:
        mid_points.append(all_points[0])
    elif all_points[0] == 3.5 or all_points[0] <= 4.4:
        good_points.append(all_points[0])
    elif all_points[0] >= 4.5:
        well_points.append(all_points[0])
    all_points.pop(0)



labels = '4.5 ve Üzeri', '3.5 - 4.4 Arası', '2.6 - 3.4 Arası', '2.5 ve Aşağı'
sizes = [len(well_points), len(good_points), len(mid_points), len(bad_points)]
explode = (0, 0.1, 0, 0)

ingiredients = ["Çok İyi Kurs", "İyi Kurs", "Orta Kurs"," Kötü Kurs"]
fig1, ax1 = plt.subplots()
ax1.set_title("Udemy Kurs Puanı Yüzdeleri")
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)

ax1.axis('equal')
ax1.legend(ingiredients,
           title="Açıklamalar",
           loc="center right")

plt.show()