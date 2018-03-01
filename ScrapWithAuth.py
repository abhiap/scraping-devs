import requests
from lxml import html
import configparser

from Extractor import Extractor
from Exporter import Exporter
from User import User


class Scrapper:
    # LOGIN_URL = "https://github.com/login/"
    # LOGOUT_URL = "https://github.com/logout"
    # SESSION_URL = "https://github.com/session"
    # SEARCH_URL = 'https://github.com/search?l=Java&o=desc&q=location%3APune&ref=advsearch&s=repositories&type=Users'
    # # l=Java&q=abhi&type=Users&o=desc&s=repositories&location=Pune'
    # USERNAME = "ajitsacc"
    # PASSWORD = "ajitsacc1"
    BASE_URL = ""
    LOGIN_URL = ""
    LOGOUT_URL = ""
    SESSION_URL = ""
    SEARCH_URL = 'https://github.com/search?l=Java&o=desc&q=location%3APune&ref=advsearch&s=repositories&type=Users'
    # l=Java&q=abhi&type=Users&o=desc&s=repositories&location=Pune'
    USERNAME = ""
    PASSWORD = ""

    def init(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.BASE_URL = config['DEFAULT']['base_url']
        self.LOGIN_URL = config['DEFAULT']['login_url']
        self.LOGOUT_URL = config['DEFAULT']['logout_url']
        self.SESSION_URL = config['DEFAULT']['gh_session_url']
        # SEARCH_URL = config['DEFAULT']['gh_search_url']
        # l=Java&q=abhi&type=Users&o=desc&s=repositories&location=Pune'
        self.USERNAME = config['DEFAULT']['gh_username']
        self.PASSWORD = config['DEFAULT']['gh_pw']

    def login(self):
        print("login>>")
        # Get login csrf token
        result = session_reqs.get(self.LOGIN_URL)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]
        # print(authenticity_token)
        # print(result.headers)
        session_key = result.cookies["_gh_sess"]
        # print(session_key)

        jar = requests.cookies.RequestsCookieJar()
        jar.set('_gh_sess', session_key, domain='.github.com', path='/')

        payload = {
            "login": self.USERNAME,
            "password": self.PASSWORD,
            "commit": "Sign in",
            "authenticity_token": authenticity_token
        }

        # Perform login
        result = session_reqs.post(self.SESSION_URL, data=payload, cookies=jar, headers=dict(referer=self.SESSION_URL))
        user_session_key = result.cookies["user_session"]
        # print(user_session_key)
        return user_session_key

    def fetch_data(self, base_url, source_page, jar, headers):
        # get no of records, then call search multiple times to extract details
        response = session_reqs.get(source_page, cookies=jar, headers=headers)

        page = response.text
        tree = html.fromstring(page)
        users_ele = list(tree.xpath("//div[@class='user-list-info ml-2']"))
        user_count_ele = tree.xpath("//div[@class='d-flex flex-justify-between border-bottom pb-3']/h3")[0]
        # print(users_ele)
        user_pages = 1
        if user_count_ele is not None:
            print(user_count_ele.text.strip())
            s = user_count_ele.text.strip()
            s = str.split(s, ' ')[0]
            newS = s.replace(',', '')
            user_pages = int(int(newS) / len(users_ele)) + 1
            print("No of pages: ", user_pages)
        # print(user_count_ele.text_content())
        users = []
        extractor = Extractor()
        for i in range(1, 3):
            print("PAGE " + str(i))
            if i == 1:
                pass
            else:
                source_page = source_page.__add__("&p=" + str(i))
                print(source_page)
                response = session_reqs.get(source_page, cookies=jar, headers=headers)
                # Extractor.extract(response, users)

            temp_users = Extractor.extract(response)
            # extract details such as no. of repositories, stars etc. of each user
            self.enrich_data(temp_users, base_url, jar, headers)
            users.extend(temp_users)

        return users

    def enrich_data(self, users, base_url, jar, headers):
        for user in users:
            print(user.variables)
            url = base_url.__add__(user.get("Username"))
            print("user url: ", url)
            # response = session_reqs.get(url, cookies=jar, headers=headers)
            response = session_reqs.get(url, headers=headers)
            Extractor.extract_details(response, user)
            # fetch from hackerrank
            hr_url = "https://www.hackerrank.com/rest/hackers/{0}/recent_challenges?limit=5" \
                     "&cursor=&response_version=v2".format(user.get("username"))
            self.fetch_hackerrank_data(hr_url, user)
            # fetch from hackerearth
        return users

    def fetch_hackerrank_data(self, url, user):
        response = session_reqs.get(url)
        print(response.content)
        data = response.json()
        print(data)
        i = len(data['models'])
        print(i)
        user.set("Challenges submitted", i)
        # print(len(data.models))

    def run(self):
        scrapper.init()

        # 1 login and get user_session
        user_session_key = scrapper.login()

        # 2 set headers, cookies
        jar = requests.cookies.RequestsCookieJar()
        # jar.set('logged_in', 'yes', domain='.github.com', path='/')
        jar.set('user_session', user_session_key, domain='.github.com', path='/')
        # jar.set('__Host-user_session_same_site', '3deRNJUKRxtZm5o5qOQmmNsGShS-moSJNFfA-6l4eHABWHre', domain='.github.com', path='/')
        # jar.set('dotcom_user', 'abhiap', domain='.github.com', path='/')
        headers = {
            'Referer': scrapper.SEARCH_URL,
            'Cache-Control': "no-cache"
        }

        # 3 get no of records, then call search multiple times to extract details
        # pages = getStat(source_page_1)
        # response = session_reqs.get(source_page, cookies=jar, headers=headers)

        # 4 extract mail id, username of each user
        users = scrapper.fetch_data(scrapper.BASE_URL, scrapper.SEARCH_URL, jar, headers)

        # 5 extract details such as no. of repositories, stars etc. of each user
        # users = scrapper.enrich_data(users, scrapper.BASE_URL, jar, headers)

        # export data to file
        Exporter.write_to_csv(users)

        result = session_reqs.get(scrapper.LOGOUT_URL)
        print(result)


if __name__ == '__main__':
    session_reqs = requests.session()
    scrapper = Scrapper()
    # scrapper.run()

    hr_url = "https://www.hackerrank.com/rest/hackers/abhiarunpatil/recent_challenges?limit=100" \
             "&cursor=&response_version=v2"
    user = User()
    scrapper.fetch_hackerrank_data(hr_url, user)

