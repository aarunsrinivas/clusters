import requests
from bs4 import BeautifulSoup
from pprint import pprint
from nlpsomething import DocSim
from flaskapp.models import Description
from flaskapp import db

def scrape():
    url = 'https://catalog.gatech.edu/coursesaz'
    coursesDict = {}
    coursesDescList = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    file = open("htmlfile.txt", "w")
    # file.write(soup.prettify().encode('utf-8').decode('ascii', 'ignore'))
    div = soup.findAll("a", href=True)
    for row in div[38:130]:
        # file.write(row.encode('utf-8').decode('ascii', 'ignore'))
        # file.write("\n")
        course = row.text
        coursesDict[course] = {}
        response2 = requests.get('https://catalog.gatech.edu' + row['href'])
        soup = BeautifulSoup(response2.text)
        div2 = soup.findAll("div", class_='courseblock')
        # print(div2)
        for row2 in div2:
            courseList = row2.findAll('strong')
            descList = row2.findAll(class_='courseblockdesc')
            for elementNumber in range(len(courseList)):
                specificCourse = courseList[elementNumber].text.split('.')
                specificCourseDesc = descList[elementNumber].text.replace('\xa0', '').replace('\n', '')
                # print(specificCourses)
                for number in range(3):
                    if number == 0:
                        courseCode = specificCourse[number].replace('\xa0', '')
                        # print(courseCode)
                    elif number == 1:
                        courseName = specificCourse[number].strip()
                        # print(courseName)
                    elif number == 2:
                        if specificCourse[number] != '':
                            courseCredits = specificCourse[number].strip()
                        else:
                            courseCredits = specificCourse[3].strip()
                        # print(courseCredits)
                try:
                    coursesDict[course][courseCode] = {'courseName': courseName, 'courseCredits': courseCredits,
                                                       'courseDesc': specificCourseDesc}
                    courseDesc = Description(keyword = courseName, description = specificCourseDesc)
                    db.session.add(courseDesc)
                    db.session.commit()
                    coursesDescList.append(specificCourseDesc)
                except:
                    pass

                # print(specificCourses)
                # print(coursesDict)
        return [coursesDict, coursesDescList]

    pprint(coursesDict)
    pprint(coursesDict, stream=file)
    file.close()

docsim = DocSim(verbose=True)
coursesInfo = scrape()
similarities = docsim.similarity_query(
    "Small group discussions with first year students are led by one or more faculty members and include a variety of foundational, motivational, and topical subjects for computationalist.",
    coursesInfo[1])
print(similarities)
#
