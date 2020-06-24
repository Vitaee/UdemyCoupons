import sys

import requests, json
from bs4 import BeautifulSoup
from sqlite3db.auth import connection as baglanti


class Udemy:
    def __init__(self):
        self.userID = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        self.baseUrl = "http://www.bugraayan.com"

        self.CourseLinks = []
        self.CourseImages = []
        self.CourseAuthors = []
        self.CourseNames = []
        self.CourseInfos = []
        self.CoursePoints = []
        self.CourseStudents = []

        self.CourseLink = False
        self.CourseImage = False
        self.CourseAuthor = False
        self.CourseName = False
        self.CourseInfo = False
        self.CoursePoint = False
        self.CourseStudent = False

        self.currentDocs = []
        self.my_json = {'udemycoupons': []}

        with open('freeudemy.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data["udemycoupons"]:
            try: self.currentDocs.append(item['Coupon Link'])
            except: pass

    def Start(self):
        i = 1
        while i <= 2:
            page = requests.get(f"{self.baseUrl}/page/{i}/", headers=self.userID)
            source = page.text
            soup = BeautifulSoup(source, 'html.parser')

            first_data = soup.find_all('div', class_='entry-content')

            for item in first_data:
                items = item.find_all('a')
                for data in items:
                    self.CourseLinks.append(data['href'])
            i += 1

        print("tüm linkler listeye atıldı.")
        self.udemyVeri()
    def udemyVeri(self):
        #Hatalı linki kaldırdık.
        prefixes = ("https://web.whatsapp.com")
        for word in self.CourseLinks[:]:
            if word.startswith(prefixes):
                self.CourseLinks.remove(word)


        a = 0
        while a <= len(self.CourseLinks):
            try:

                page = requests.get(self.CourseLinks[a], headers=self.userID)
                source = page.text
                soup = BeautifulSoup(source, 'html.parser')
            except:
                pass


            try:print(f"\tİncelenen {a}. Link => {self.CourseLinks[a]}")
            except:pass

            try:
                if self.CourseLinks[a] in self.currentDocs:
                    print("Aynı link denk geldi!")
                    print(f"{self.CourseLinks[a]} aynı link silindi!")
                    del self.CourseLinks[a]
                    pass
                else:
                    #Eğitim Adı
                    try:
                        course_name = soup.find('h1',class_='clp-lead__title')
                        self.CourseName = course_name.text.rstrip()
                        self.CourseNames.append(course_name.text.rstrip())

                        #Eğitim Link
                        self.CourseLink = self.CourseLinks[a]

                    except:
                        print("Kupon linki hatalı!")
                        del self.CourseLinks[a]
                        pass


                    #Eğitim Resmi
                    try:
                        course_img = soup.find_all('img')
                        self.CourseImage = course_img[1]['src']
                        self.CourseImages.append(course_img[1]['src'])
                    except: pass

                    #Eğitim Durumu
                    try:
                        course_info = soup.find_all('div',class_='price-text')
                        if not course_info:
                            data = soup.find_all('meta', content_='')

                            self.CourseInfo = data[15]['content'][:8]
                            self.CourseInfos.append(data[15]['content'][:8])
                        else:
                            for item in course_info:
                                items = item.find('span')

                                self.CourseInfo = items.text.strip()
                                self.CourseInfos.append(items.text.strip())
                    except: pass

                    try:
                        data = soup.find('span', attrs={'data-purpose': 'rating-number'})
                        if not data:
                            new_data = soup.find_all('div',class_='rate-count')
                            for i in new_data:
                                items = i.find('span')
                                self.CoursePoint = items.text[:4].strip().replace(",", ".")
                                self.CoursePoints.append(items.text[:4].strip().replace(",", "."))
                                break
                        else:
                            course_point = data.text.replace(",", ".")
                            self.CoursePoint = course_point
                            self.CoursePoints.append(course_point)
                    except: pass


                    #Eğitmen Adı
                    try:
                        course_author = soup.find_all('div', class_='instructor-links--instructor-links--3d8_F')
                        if not course_author:
                            author_name = soup.find_all('span',attrs={'data-purpose':'instructor-name-top'})
                            for i in author_name:
                                items = i.find('a')
                                self.CourseAuthor = items.text.strip()
                                self.CourseAuthors.append(items.text.strip())
                        else:
                            for item in course_author:
                                items = item.find('a')
                                self.CourseAuthor = items.text.strip()
                                self.CourseAuthors.append(items.text.strip())
                    except: pass

                    #Eğitime Kayıtlı Öğrenci Sayısı
                    try:
                        course_students = soup.find_all('div', class_='enrollment')
                        if not course_students:
                            students = soup.find('div',attrs={'data-purpose':'enrollment'})
                            self.CourseStudent = students.text
                            self.CourseStudents.append(students.text.rstrip())
                        else:
                            self.CourseStudent = course_students.text
                            self.CourseStudents.append(course_students.text.rstrip())
                    except:
                        last_studenst = soup.find('div',attrs={'data-purpose':'enrollment'})
                        self.CourseStudents.append(last_studenst.text.rstrip())
                        self.CourseStudent = last_studenst.text.rstrip()
                        pass


                    data = {"Coupon Link": self.CourseLink,
                                "Course Name": self.CourseName,
                                "Course Image": self.CourseImage,
                                "Course Info": self.CourseInfo,
                                "Course Point": self.CoursePoint,
                                "Course Author": self.CourseAuthor,
                                "Course Students": self.CourseStudent}
                    self.my_json["udemycoupons"].append(data)

                    self.save(self.CourseLink, self.CourseName, self.CourseImage,
                                  self.CourseInfo, self.CoursePoint, self.CourseAuthor,
                                  self.CourseStudent)

                    a += 1
            except:
                print("incelenen link hatası")
                a += 1


        print("Döngü bitti veriler DB'ye aktarılıyor.")
        self.saveResults()
    def save(self,couponLinks, courseName, courseImg,courseInf,coursePoint, courseAuthor,courseStudents):
        with open('freeudemy.json', 'w', encoding='UTF-8') as file:
            json.dump(self.my_json, file, indent=2, ensure_ascii=False)


    def saveResults(self):
        #Hatalı verileri silme işlemi.
        prefixes = ("https://www.udemy.com/stat")
        for word in self.CourseImages[:]:
            if word.startswith(prefixes):
                self.CourseImages.remove(word)

        prefixes = ("https://", "summary")
        for word in self.CourseInfos[:]:
            if word.startswith(prefixes):
                self.CourseInfos.remove(word)
                
        conn = baglanti()

        #Saving to SQLite

        for index, item in enumerate(self.CourseLinks, 0):
            sqlQuery = """INSERT INTO FreeUdemy
                                      (CourseNames, CourseLinks, CourseImages, CourseAuthors, CourseInfos, CoursePoints, CourseStudents)
                                      VALUES (?, ?, ?, ?, ?, ?, ?);"""
            data = (self.CourseNames[index],self.CourseLinks[index], self.CourseImages[index],self.CourseAuthors[index],self.CourseInfos[index],self.CoursePoints[index],self.CourseStudents[index])
            conn.cursor().execute(sqlQuery, data)
            conn.commit()
        print("Veri aktarımı tamamlandı.")
   


if __name__ == '__main__':
    Udemy().Start()
