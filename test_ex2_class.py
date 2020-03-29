import unittest
from unittest.mock import patch
import ex2_class
from benedict import benedict
import copy


class TestUserPostParser(unittest.TestCase):

    def setUp(self):
        self.no_urls_class = ex2_class.UserPostParser()

        self.sample_post = dict(userId=1, id=1,
                                title="sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                                body="quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto")

        self.sample_user_no_posts = dict(id=1, name='Leanne Graham', username='Bret', email='Sincere@april.biz',
                                         address=dict(street='Kulas Light', suite='Apt. 556', city='Gwenborough',
                                                      zipcode='92998-3874', geo={'lat': -37.3159, 'lng': 81.1496}),
                                         phone='1-770-736-8031 x56442', website='hildegard.org',
                                         company=dict(name='Romaguera-Crona',
                                                      catchPhrase='Multi-layered client-server neural-net',
                                                      bs='harness real-time e-markets'), posts=[])
    def tearDown(self):
        None

    def test_get_data_from_url_status_code_200(self):
        """ check reposnse when correct status_code """
        self.sample_user_no_posts["address"]["geo"]["lat"] = '-37.3159'
        self.sample_user_no_posts["address"]["geo"]["lng"] = '81.1496'
        del self.sample_user_no_posts["posts"]
        with patch('ex2_class.requests.get') as mocked_get:  # patch used with context menager
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.text = """[
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  }
]"""
            datalist = self.no_urls_class.get_data_from_url('test.url')
            self.assertEqual(datalist, [self.sample_user_no_posts])

    @patch('ex2_class.requests')  # patch used with decorator
    def test_get_data_from_url_status_code_not_200(self, mocked_get):
        """ check reposnse when incorrect status_code """
        mocked_get.get.return_value.status_code = 201
        datalist = self.no_urls_class.get_data_from_url('test.url')
        self.assertEqual(datalist, [])


    def test_get_data_from_url_timeout(self):
        """ check reposnse except timeout """
        with patch('ex2_class.requests.get') as mocked_get:
            mocked_get.side_effect = ex2_class.requests.exceptions.Timeout
            result = self.no_urls_class.get_data_from_url('test.url')
            self.assertRaises(ex2_class.requests.exceptions.Timeout)
            self.assertEqual(result, [])

    def test_get_data_from_url_except_other(self):
        """ check reposnse except other
        all exceptions of requests inherit from requests.exceptions.RequestException
        """
        with patch('ex2_class.requests.get') as mocked_get:
            mocked_get.side_effect = ex2_class.requests.exceptions.RequestException
            result = self.no_urls_class.get_data_from_url('test.url')
            self.assertRaises(ex2_class.requests.exceptions.Timeout)
            self.assertEqual(result, [])

    def test_correct_geo_values_benedict(self):
        """ check correct work"""
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.users[0]["address"]["geo"]["lat"] = '-37.3159'
        self.no_urls_class.users[0]["address"]["geo"]["lng"] = '81.1496'
        self.no_urls_class.users = list(map(benedict, self.no_urls_class.users))  # change to benedict as in program
        self.no_urls_class.correct_geo_values()
        self.assertIsInstance(self.no_urls_class.users[0]["address"]["geo"]["lat"], float)
        self.assertIsInstance(self.no_urls_class.users[0]["address"]["geo"]["lng"], float)

    def test_correct_geo_values_other(self):
        """ check work when not benedict class or weird string"""
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.users[0]["address"]["geo"]["lat"] = '-37.3159'
        self.no_urls_class.users[0]["address"]["geo"]["lng"] = '81.1496'
        self.no_urls_class.correct_geo_values()
        self.assertIsInstance(self.no_urls_class.users[0]["address"]["geo"]["lat"], str)
        self.assertIsInstance(self.no_urls_class.users[0]["address"]["geo"]["lng"], str)

    def test_correct_geo_values_except(self):
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.users[0]["address"]["geo"]["lat"] = 'wierd string'
        self.no_urls_class.users[0]["address"]["geo"]["lng"] = 'hmmm'
        self.no_urls_class.users = list(map(benedict, self.no_urls_class.users))  # change to benedict as in program
        self.no_urls_class.correct_geo_values()
        self.assertRaises(ValueError)
        self.assertIsInstance(self.no_urls_class.users[0]["address"]["geo"]["lat"], str)
        self.assertIsInstance(self.no_urls_class.users[0]["address"]["geo"]["lng"], str)

    def test_parse_users_posts_correct(self):
        """ check parse with good posts """
        self.no_urls_class.users = [self.sample_user_no_posts]
        result = self.no_urls_class.parse_users_posts([self.sample_post])
        self.assertEqual(self.no_urls_class.users[0]['posts'], [self.sample_post])
        self.assertEqual(result, True)

    def test_parse_users_posts_incorrect(self):
        """ check parse with bad posts or no users """
        self.no_urls_class.users = []
        result = self.no_urls_class.parse_users_posts([self.sample_post])
        self.assertEqual(self.no_urls_class.users, [])
        self.assertEqual(result, None)

        self.no_urls_class.users = [self.sample_user_no_posts]
        posts = []
        result = self.no_urls_class.parse_users_posts(posts)
        self.assertEqual(self.no_urls_class.users[0]['posts'], [])
        self.assertEqual(result, None)

        self.no_urls_class.users = [self.sample_user_no_posts]
        result = self.no_urls_class.parse_users_posts()
        self.assertEqual(self.no_urls_class.users[0]['posts'], [])
        self.assertEqual(result, None)

    def test_number_of_posts_of_users_no_users(self):
        # no users
        num_of_posts_str = self.no_urls_class.number_of_posts_of_users()
        self.assertEqual(num_of_posts_str, None)

    def test_number_of_posts_of_users_no_posts(self):
        # only users, no posts, check if inside for
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.users[0]['posts'] = []
        num_of_posts_str = self.no_urls_class.number_of_posts_of_users()
        self.assertEqual(num_of_posts_str, [])

        self.no_urls_class.users = [self.sample_user_no_posts]
        del self.no_urls_class.users[0]['posts']
        num_of_posts_str = self.no_urls_class.number_of_posts_of_users()
        self.assertEqual(num_of_posts_str, [])

        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.users[0]['posts'] = None
        num_of_posts_str = self.no_urls_class.number_of_posts_of_users()
        self.assertEqual(num_of_posts_str, [])

    def test_number_of_posts_of_users_post(self):
        # user with one post, check exact string
        self.sample_user_no_posts['posts'] = [self.sample_post]
        self.no_urls_class.users = [self.sample_user_no_posts]
        num_of_posts_str = self.no_urls_class.number_of_posts_of_users()
        self.assertEqual(num_of_posts_str, ["Bret napisał(a) 1 postów"])
    # could also check both tests with 2 users, one with post and one without

    def test_get_not_unique_title_list_correct(self):
        """ check number of title lists """
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.parse_users_posts([self.sample_post])
        result = self.no_urls_class.get_not_unique_title_list()
        self.assertEqual(result, [])

        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.parse_users_posts([self.sample_post, self.sample_post])
        result = self.no_urls_class.get_not_unique_title_list()
        self.assertEqual(result, ["sunt aut facere repellat provident occaecati excepturi optio reprehenderit"])

    def test_get_not_unique_title_list_no_users(self):
        """ check function when no users in class """
        result = self.no_urls_class.get_not_unique_title_list()
        self.assertEqual(result, None)

    def test_find_closest_user_empty_users(self):
        """ check if works when users list empty """
        result = self.no_urls_class.find_closest_user(self.sample_user_no_posts)
        self.assertEqual(result, None)

    def test_find_closest_user_normal_work(self):
        """ check if finds closest user """
        user_00 = self.sample_user_no_posts
        user_00["address"]["geo"]["lat"] = 0.0
        user_00["address"]["geo"]["lng"] = 0.0
        user_1010 = copy.deepcopy(self.sample_user_no_posts)
        user_1010["address"]["geo"]["lat"] = 10.0
        user_00["address"]["geo"]["lng"] = 10.0
        user_3030 = copy.deepcopy(self.sample_user_no_posts)
        user_3030["address"]["geo"]["lat"] = 30.0
        user_3030["address"]["geo"]["lng"] = 30.0
        self.no_urls_class.users = [user_1010, user_3030]
        result = self.no_urls_class.find_closest_user(user_00)
        self.assertEqual(result, user_1010)

    def test_add_users_no_urls(self):
        """ check fucntion when no urls provided """
        result = self.no_urls_class.add_users()
        self.assertEqual(result, None)

    def test_add_users_argument_url(self):
        """ check if works with url provided with argument """
        user1 = copy.deepcopy(self.sample_user_no_posts)
        with patch('ex2_class.UserPostParser.get_data_from_url') as mocked_get_data:
            mocked_get_data.return_value = [self.sample_user_no_posts]
            result = self.no_urls_class.add_users('test.url')
            self.assertEqual(self.no_urls_class.users, [user1])
            self.assertEqual(result, 2)

    def test_add_users_self_url(self):
        """ check if works with url from self """
        user1 = copy.deepcopy(self.sample_user_no_posts)
        self.no_urls_class.user_url = 'test.url'
        with patch('ex2_class.UserPostParser.get_data_from_url') as mocked_get_data:
            mocked_get_data.return_value = [self.sample_user_no_posts]
            result = self.no_urls_class.add_users()
            self.assertEqual(self.no_urls_class.users, [user1])
            self.assertEqual(result, 1)

    def test_add_posts_no_url(self):
        """ check if return null if no URL provided """
        result = self.no_urls_class.add_posts()
        self.assertEqual(result, None)

    def test_add_posts_argument_url(self):
        """ check if return null if no URL provided """
        self.no_urls_class.users = [self.sample_user_no_posts]
        with patch('ex2_class.UserPostParser.get_data_from_url') as mocked_get_data:
            mocked_get_data.return_value = [self.sample_post]
            result = self.no_urls_class.add_posts('test.url')
            self.assertEqual(result, 2)
            self.assertEqual(self.no_urls_class.users[0]['posts'], [self.sample_post])

    def test_add_posts_self_url(self):
        """ check if return null if no URL provided """
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.posts_url = 'test.url'
        with patch('ex2_class.UserPostParser.get_data_from_url') as mocked_get_data:
            mocked_get_data.return_value = [self.sample_post]
            result = self.no_urls_class.add_posts()
            self.assertEqual(result, 1)
            self.assertEqual(self.no_urls_class.users[0]['posts'], [self.sample_post])

    def test_remove_repeated_users_tripled_users(self):
        """ checks if method removes repeated users (by ID) """
        self.no_urls_class.users = [self.sample_user_no_posts, self.sample_user_no_posts, self.sample_user_no_posts]
        self.no_urls_class.remove_repeated_users()
        self.assertEqual(self.no_urls_class.users, [self.sample_user_no_posts])

    def test_remove_repeated_users_single_user(self):
        """ checks if method does not remove single user (by ID) """
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.remove_repeated_users()
        self.assertEqual(self.no_urls_class.users, [self.sample_user_no_posts])

    def test_remove_repeated_posts_tripled_post(self):
        """ checks if method removes repeated posts of users (by ID) """
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.users[0]['posts']=[self.sample_post, self.sample_post, self.sample_post]
        self.no_urls_class.remove_repeated_posts()
        self.assertEqual(self.no_urls_class.users[0]['posts'], [self.sample_post])

    def test_remove_repeated_posts_single_post(self):
        """ checks if method does not remove single post of user (by ID) """
        self.no_urls_class.users = [self.sample_user_no_posts]
        self.no_urls_class.users[0]['posts'] = [self.sample_post]
        self.no_urls_class.remove_repeated_posts()
        self.assertEqual(self.no_urls_class.users[0]['posts'], [self.sample_post])


if __name__ == '__main__':
    unittest.main()
