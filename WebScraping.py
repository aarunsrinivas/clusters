import requests
from bs4 import BeautifulSoup
from pprint import pprint


class Search:
    def __init__(self):
        self.url = 'https://catalog.gatech.edu/coursesaz'

    def pretty(d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                d.pretty(value, indent + 1)
            else:
                print('\t' * (indent + 1) + str(value))

    def scrape(self):
        coursesDict = {}
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        file = open("htmlfile.txt", "w")
        # file.write(soup.prettify().encode('utf-8').decode('ascii', 'ignore'))
        div = soup.findAll("a", href=True)
        for row in div[38:130]:
            # file.write(row.encode('utf-8').decode('ascii', 'ignore'))
            # file.write("\n")
            course = row.text
            coursesDict[course] = {}
            response2 = requests.get('https://catalog.gatech.edu' + row['href'])
            soup = BeautifulSoup(response2.text, "lxml")
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
                    coursesDict[course][courseCode] = {'courseName': courseName, 'courseCredits': courseCredits,
                                                       'courseDesc': specificCourseDesc}
                    # print(specificCourses)
                    print(coursesDict)

        pprint(coursesDict)
        pprint(coursesDict, stream=file)
        file.close()

newSearch = Search()
newSearch.scrape()

