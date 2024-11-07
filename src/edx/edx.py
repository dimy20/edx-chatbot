
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv

def clean_overview(overview):
    soup = BeautifulSoup(overview, "html.parser")
    overview_text = soup.get_text()
    overview_text = " ".join(overview_text.split())
    return overview_text

class EdxClient:
    def __init__(self, host, access_token):
        self.base_url = host + "/api"
        self.access_token = access_token
        self.courses_url = f"{self.base_url}/courses/v1/courses"

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_all_courses(self):
        res = requests.get(url=self.courses_url, headers=self.headers)
        if res.status_code == 200:
            data = json.loads(res.content)
            return data["results"] if "results" in data else []
        else:
            raise ValueError("Failed to get all courses")

    #No es la mejor forma de hacer esto pero bue
    def find_course_by_name(self, course_name: str):
        courses = self.get_all_courses()
        index = - 1
        for i, course in enumerate(courses):
            if course["name"] == course_name:
                index = i
                break
            
        if index != -1:
            course_id = courses[index]["id"]
            course_data = self.get_course_metadata(course_id)
            return course_data
        else:
            return None

    def get_courseware_course(self, course_id : str):
        url = self.base_url + f"/courseware/course/{course_id}"
        res = requests.get(url=url, headers=self.headers)
        if res.status_code == 200:
            return json.loads(res.content)
        else:
            raise ValueError(f"Http error : {res.status_code}")

    def get_course_metadata(self, course_id: str):
        course_metadata_url = f"{self.base_url}/courses/v1/courses/{course_id}/"
        res = requests.get(url=course_metadata_url, headers=self.headers)
        if res.status_code == 200:
            return json.loads(res.content)
        else:
            raise ValueError(f"Http error : {res.status_code}")

    def get_course_overview(self, course_id):
        data = self.get_course_metadata(course_id)
        return clean_overview(data["overview"])