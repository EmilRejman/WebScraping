import requests
from bs4 import BeautifulSoup
import ast
from collections import Counter, defaultdict
from geopy.distance import distance
from benedict import benedict

"""
Posts and Users overreview (ispect the HTML):
All the data we want to extract from is inside the body part of html in preformated text tag.
The data we want to gather is table of dicts.
"""


# task 1 : merge data

class UserPostParser:

    def __init__(self, user_url=None, posts_url=None):
        self.user_url = user_url  # remember the urls for probable future operations
        self.posts_url = posts_url
        self.users = []

    @staticmethod
    def get_data_from_url(url):
        """ gets data from URL, part it with BeautifulSoup
        and change it to python datatype"""

        try:
            response = requests.get(url, timeout=5)  #
        except requests.exceptions.Timeout as e:
            print(f'timout error of url: {url}, code: {e}')
            return []
        except requests.exceptions.RequestException as e:  # all request exceptions inherit from RequestException
            print(f'some error of request from url: {url}, code: {e}')
            return []

        if response.status_code == 200:  # if correct response
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.contents[0]
            data_list = ast.literal_eval(data)
            return data_list
        else:
            print(f'bad response status code, status code: {response.status_code}')
            return []

    def correct_geo_values(self):
        """ converts geo values from string to float """
        for user in self.users:
            if 'address.geo.lat' and 'address.geo.lng' in user:
                try:
                    user["address"]["geo"]["lat"] = float(user["address"]["geo"]["lat"])
                    user["address"]["geo"]["lng"] = float(user["address"]["geo"]["lng"])
                except ValueError:
                    print("Not a float")

    def parse_users_posts(self, posts=None):
        """ connects posts to related users """
        if (self.users != []) and (posts != []) and (posts is not None):
            for user in self.users:  # add posts to each user
                [ user['posts'].append(post) for post in posts if post['userId'] == user['id']]
            print('data parsed')
            return True
        else:
            print(f'users or posts data empty, cant do parsing')
            return None

    def number_of_posts_of_users(self):
        """ returns list of string of format '<username> napisał(a) <count_posts>'
        for each user in list      """
        if len(self.users) == 0:
            print('no users, cant get number of posts')
            return

        table_of_strings = []

        for user in self.users:
            if 'posts' not in user or user['posts'] == [] or user['posts'] is None:
                # user has no posts
                continue

            table_of_strings.append(f"{user['username']} napisał(a) {len(user['posts'])} postów")

        return table_of_strings

    def get_not_unique_title_list(self):
        """ returns repeated titles of posts """
        if len(self.users) == 0:
            print('data is not valid, cant get not uniqe title list\n')
            return

        post_list = []
        [post_list.extend(user['posts']) for user in self.users]
        title_list = [post['title'] for post in post_list]
        notUniqueTitleList = [notUniqueTitle for (notUniqueTitle, v) in Counter(title_list).items() if v > 1]
        print(f"lista nieunikalnych tytułów postów: {notUniqueTitleList}")
        return notUniqueTitleList

    def find_closest_user(self, user_distance_to):
        """ finds closests user from base to one placed as argument and returns closest user to this one"""
        if len(self.users) == 0:
            print('no users on list, cant find closest user')
            return

        distance_list_km = [distance((user["address"]["geo"]["lat"], user["address"]["geo"]["lng"]),
                                     (user_distance_to["address"]["geo"]["lat"],
                                      user_distance_to["address"]["geo"]["lng"])).km
                            for user in self.users]

        raw_without_zero = [distance_km for distance_km in distance_list_km if distance_km > 0]
        index = [i for i, x in enumerate(distance_list_km) if x == min(raw_without_zero)]
        print(f"najbliższym sąsiadem {user_distance_to['username']} jest {self.users[int(index[0])]['username']} ")
        return self.users[int(index[0])]

    def add_users(self, url=None):
        """ extends users with users downloaded from url """
        if url is None:
            if self.user_url is None:
                print('nie podano ścieżki użytkowników')
                return
            else:
                self.users.extend(self.get_data_from_url(self.user_url))
                self.remove_repeated_users()
                for user in self.users:  # create field for posts
                    user['posts'] = []
                self.users = list(map(benedict, self.users))  # make dicts benedict for easier work
                self.correct_geo_values()
                return 1
        else:
            self.users.extend(self.get_data_from_url(url))
            self.remove_repeated_users()
            for user in self.users:  # create field for posts
                user['posts'] = []
            self.users = list(map(benedict, self.users))
            self.correct_geo_values()
            return 2

    def add_posts(self, url=None):
        """ download posts from URL and adds them to users """
        if url is None:
            if self.posts_url is None:
                print('nie podano ścieżki postów')
                return
            else:
                posts = self.get_data_from_url(self.posts_url)
                self.parse_users_posts(posts)
                self.remove_repeated_posts()
                return 1
        else:
            posts = self.get_data_from_url(url)
            self.parse_users_posts(posts)
            self.remove_repeated_posts()
            return 2

    def remove_repeated_users(self):
        """ removes users with the same ID, deletes later added users """
        d = defaultdict(list)
        for i in self.users:
            d[i['id']].append(i) # append user dict to dict with key of specyfic "id"

        for key, values in d.items():
            if len(values) > 1:
                for val_to_del in values[1:]:  # delete older users (further on list)
                    self.users.remove(val_to_del)
        # [ [self.users.remove(val_to_del) for val_to_del in values[1:]] for key, values in d.items() if len(values) > 1]
        # less visible

    def remove_repeated_posts(self):
        """ removes posts with the same ID, deletes later added pots """
        for user in self.users:
            d = defaultdict(list)
            for post in user['posts']:
                d[post['id']].append(post)

            for key, values in d.items():
                if len(values) > 1:
                    for val_to_del in values[1:]:  # delete older users (further on list)
                        user['posts'].remove(val_to_del)
