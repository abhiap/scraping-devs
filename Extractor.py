import requests

from lxml import html
from User import User


class Extractor:

    # @staticmethod
    # def call_and_extract(session_reqs, base_url, source_page, jar, headers, users):
    #     response = session_reqs.get(source_page, cookies=jar, headers=headers)
    #     # users.append(extract(response))
    #     users = Extractor.extract(response)
    #     print("users in call_extr: ", len(users))
    #     for user in users:
    #         url = base_url.__add__(user.get("username"))
    #         print("user url: ", url)
    #         response2 = session_reqs.get(url, cookies=jar, headers=headers)
    #         Extractor.extract_details(response2, user)

    @staticmethod
    def extract(response):
        page = response.text
        tree = html.fromstring(page)
        users_ele = list(tree.xpath("//div[@class='user-list-info ml-2']"))
        users = []
        for u in users_ele:
            # print(u.text_content())
            username, name, email = "", "", ""
            if u.find("a") is not None:
                username_ele = u.find("a").attrib
                # print("uname ele", username_ele)
                if username_ele:
                    # print(username_ele.items())
                    username = username_ele['href']

            name_ele = u.find_class("f4 ml-1")
            if name_ele:
                name = name_ele[0].text_content()

            email_ele = u.find_class("muted-link")
            if email_ele:
                email = email_ele[0].text_content()

            # print(name + " | " + email)
            user = User()
            user.set("Username", username)
            user.set("Name", name)
            user.set("Email", email)
            users.append(user)

        return users

    @staticmethod
    def extract_details(response, user):
        page = response.text
        # print("page: ", page)
        tree = html.fromstring(page)
        stats_ele = list(tree.xpath("//nav[@class='UnderlineNav-body']/a"))
        for stat in stats_ele:
            # if stat.attrib['title'] == "Repositories":
            #     stat_ele = stat.find_class("Counter")[0]
            #     # print("repos: ", stat_ele.text_content().strip())
            #     repos = stars = Extractor.convert_to_num(stat_ele.text_content().strip())
            #     user.set("repositories", repos)
            # elif stat.attrib['title'] == "Stars":
            #     stat_ele = stat.find_class("Counter")[0]
            #     stars = Extractor.convert_to_num(stat_ele.text_content().strip())
            #     user.set("stars", stars)
            # elif stat.attrib['title'] == "Followers":
            #     stat_ele = stat.find_class("Counter")[0]
            #     user.set("followers", stat_ele.text_content().strip())
            # elif stat.attrib['title'] == "Following":
            #     stat_ele = stat.find_class("Counter")[0]
            #     user.set("following", stat_ele.text_content().strip())
            if stat.attrib['title'] != "Overview":
                stat_ele = stat.find_class("Counter")[0]
                num = Extractor.convert_to_num(stat_ele.text_content().strip())
                user.set(stat.attrib['title'], num)

        print(user.variables)

    @staticmethod
    def convert_to_num(n):
        if n.endswith('k'):
            n = n.replace('k', '')
            num = float(n) * 1000
            return int(num)
        elif n.endswith('m'):
            n = n.replace('m', '')
            num = float(n) * 1000000
            return int(num)
        else:
            return int(n)


if __name__ == '__main__':
    session_reqs = requests.session()
    result = session_reqs.get("https://github.com/RahulSDeshpande")
    user = User()
    Extractor.extract_details(result, user)