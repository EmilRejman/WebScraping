from app import ex2_class
import pytest
from benedict import benedict
import copy

""" Tests done with usage of pytest """


## TESTS ##


class TestEx2Class():

    # using indirect parametrization to make DRY test, group in conftest.py
    @pytest.mark.parametrize("group", ["no_users", "no_posts", "posts_None"], indirect=True)
    def test_parse_users_with_posts_incorrect(self, group):
        group[0].users = group[1]

        result = group[0].parse_users_posts(group[2])

        assert result == False

    def test_parse_users_with_posts(self, basic_user, basic_class, basic_post):
        """ check parse with good posts """
        basic_class.users = [basic_user]

        result = basic_class.parse_users_posts([basic_post])

        assert basic_class.users[0]['posts'] == [basic_post]
        assert result == True

    def test_get_data_from_url_with_ok_status_code(self, mocker, basic_user, basic_class):
        "check response when status code is correct"
        basic_user["address"]["geo"]["lat"] = str(basic_user["address"]["geo"]["lat"])
        basic_user["address"]["geo"]["lng"] = str(basic_user["address"]["geo"]["lng"])
        mocked_get = mocker.patch('app.ex2_class.requests.get')
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = "[\n" + str(basic_user) + "\n]"

        datalist = basic_class.get_data_from_url('test.url')

        assert datalist == [basic_user]

    def test_get_data_from_url_with_nok_status_code(self, mocker, basic_user, basic_class):
        "check response when status code is incorrect"
        basic_user["address"]["geo"]["lat"] = str(basic_user["address"]["geo"]["lat"])
        basic_user["address"]["geo"]["lng"] = str(basic_user["address"]["geo"]["lng"])
        mocked_get = mocker.patch('app.ex2_class.requests.get')
        mocked_get.return_value.status_code = 201
        mocked_get.return_value.text = "[\n" + str(basic_user) + "\n]"

        datalist = basic_class.get_data_from_url('test.url')

        assert datalist == []

    @pytest.mark.parametrize("exception",
                             [ex2_class.requests.exceptions.Timeout, ex2_class.requests.exceptions.RequestException])
    def test_get_data_from_url_with_except(self, mocker, basic_user, basic_class, exception):
        "check response when request.get throws exception"
        basic_user["address"]["geo"]["lat"] = str(basic_user["address"]["geo"]["lat"])
        basic_user["address"]["geo"]["lng"] = str(basic_user["address"]["geo"]["lng"])
        mocked_get = mocker.patch('app.ex2_class.requests.get')
        mocked_get.side_effect = exception

        datalist = basic_class.get_data_from_url('test.url')

        assert datalist == []

    def test_correct_geo_values_users_not_benedict(self, basic_user, basic_class):
        """" check work when not benedict class"""
        basic_class.users = [basic_user]
        basic_class.users[0]["address"]["geo"]["lat"] = '-37.3159'
        basic_class.users[0]["address"]["geo"]["lng"] = '81.1496'

        sut = basic_class.correct_geo_values()

        assert isinstance(basic_class.users[0]["address"]["geo"]["lat"], str)
        assert isinstance(basic_class.users[0]["address"]["geo"]["lng"], str)

    def test_correct_geo_values_are_invalid(self, basic_user, basic_class):
        """" check work when values are incorrect"""
        basic_class.users = [basic_user]
        basic_class.users[0]["address"]["geo"]["lat"] = 'wierd string'
        basic_class.users[0]["address"]["geo"]["lng"] = {'text': 123}
        basic_class.users = list(map(benedict, basic_class.users))  # change to benedict as in program

        sut = basic_class.correct_geo_values()

        assert isinstance(basic_class.users[0]["address"]["geo"]["lat"], str)
        assert isinstance(basic_class.users[0]["address"]["geo"]["lng"], dict)

    def test_correct_geo_values_correct(self, basic_user, basic_class):
        """" check work with excepted strings"""
        basic_class.users = [basic_user]
        basic_class.users[0]["address"]["geo"]["lat"] = '-37.3159'
        basic_class.users[0]["address"]["geo"]["lng"] = '81.1496'
        basic_class.users = list(map(benedict, basic_class.users))  # change to benedict as in program

        sut = basic_class.correct_geo_values()

        assert isinstance(basic_class.users[0]["address"]["geo"]["lat"], float)
        assert isinstance(basic_class.users[0]["address"]["geo"]["lng"], float)

    @pytest.mark.parametrize("dele, posts", [(False, []), (False, None), (True, None)])
    def test_number_of_posts_of_users_no_posts(self, basic_user, basic_class, dele, posts):
        # only users, no posts, check if inside for
        basic_class.users = [basic_user]
        if dele:
            del basic_class.users[0]['posts']
        else:
            basic_class.users[0]['posts'] = posts

        num_of_posts_str = basic_class.number_of_posts_of_users()

        assert num_of_posts_str == []

    def test_number_of_posts_of_users_one_post(self, basic_user, basic_class, basic_post):
        basic_user['posts'] = [basic_post]
        print(basic_user)
        basic_class.users = [basic_user]

        num_of_posts_str = basic_class.number_of_posts_of_users()

        assert num_of_posts_str == ["Bret napisał(a) 1 postów"]

    @pytest.mark.parametrize("posts_table, result",
                             [("one_post", "none"), ("two_posts", "post"), ("three_posts", "post")],
                             indirect=["posts_table", "result"])
    def test_get_not_unique_title_list_correct(self, basic_user, basic_class, posts_table, result):
        """ check number of title lists with different number of posts combinations """
        basic_class.users = [basic_user]
        basic_class.parse_users_posts(posts_table)

        result_inner = basic_class.get_not_unique_title_list()

        assert result_inner == result

    def test_get_not_unique_title_list_no_user(self, basic_class):
        """ check number of title lists when no users in class """
        result = basic_class.get_not_unique_title_list()

        assert result == []

    def test_find_closest_user_empty_users(self, basic_user, basic_class, ):
        """ check if works when users list empty """
        result = basic_class.find_closest_user(basic_user)

        assert result == None

    @pytest.mark.parametrize("pos", [10.001, -10.001, 11.0, -11.0])
    def test_find_closest_user_normal_work(self, basic_user, basic_class, pos):
        """ check if finds closest user """
        user_00 = copy.deepcopy(basic_user)
        user_00["address"]["geo"]["lat"] = 0.0
        user_00["address"]["geo"]["lng"] = 0.0
        user_1010 = copy.deepcopy(basic_user)
        user_1010["address"]["geo"]["lat"] = 10.0
        user_1010["address"]["geo"]["lng"] = 10.0
        user_pos = copy.deepcopy(basic_user)
        user_pos["address"]["geo"]["lat"] = pos
        user_pos["address"]["geo"]["lng"] = pos
        basic_class.users = [user_1010, user_pos]

        result = basic_class.find_closest_user(user_00)

        assert result == user_1010

    def test_add_users_no_urls(self, basic_class):
        """ check fucntion when no urls provided """
        result = basic_class.add_users()

        assert result == 0

    def test_add_users_argument_url(self, mocker, basic_class, basic_user):
        """ check if works with url provided with argument """
        user1 = copy.deepcopy(basic_user)
        mocked_get_data = mocker.patch('app.ex2_class.UserPostParser.get_data_from_url')
        mocked_get_data.return_value = [basic_user]

        result = basic_class.add_users('test.url')

        assert basic_class.users == [user1]
        assert result == 2

    def test_add_users_self_url(self, mocker, basic_class, basic_user):
        """ check if works with url from self """
        user1 = copy.deepcopy(basic_user)
        basic_class.user_url = 'test.url'
        mocked_get_data = mocker.patch('app.ex2_class.UserPostParser.get_data_from_url')
        mocked_get_data.return_value = [basic_user]

        result = basic_class.add_users()

        assert basic_class.users == [user1]
        assert result == 1

    def test_add_posts_no_url(self, basic_class, basic_user):
        """ check if return null if no URL provided """
        basic_class.users = [basic_user]

        result = basic_class.add_posts()

        assert result == 0
        assert basic_class.users[0]['posts'] == []

    def test_add_posts_argument_url(self, mocker, basic_class, basic_user, basic_post):
        """ check if return null if no URL provided """
        basic_class.users = [basic_user]
        mocked_get_data = mocker.patch('app.ex2_class.UserPostParser.get_data_from_url')
        mocked_get_data.return_value = [basic_post]

        result = basic_class.add_posts('test.url')

        assert result == 2
        assert basic_class.users[0]['posts'] == [basic_post]

    def test_add_posts_argument_url_empty(self, mocker, basic_class, basic_user):
        """ check if return null if no URL provided """
        basic_class.users = [basic_user]
        mocked_get_data = mocker.patch('app.ex2_class.UserPostParser.get_data_from_url')
        mocked_get_data.return_value = []

        result = basic_class.add_posts('test.url')

        assert result == 2
        assert basic_class.users[0]['posts'] == []

    def test_add_posts_self_url(self, mocker, basic_class, basic_user, basic_post):
        """ check if return null if no URL provided """
        basic_class.users = [basic_user]
        basic_class.posts_url = 'test.url'
        mocked_get_data = mocker.patch('app.ex2_class.UserPostParser.get_data_from_url')
        mocked_get_data.return_value = [basic_post]

        result = basic_class.add_posts()

        assert result == 1
        assert basic_class.users[0]['posts'] == [basic_post]

    @pytest.mark.parametrize("users", ["single_user", "many_users"], indirect=True)
    def test_remove_repeated_users(self, basic_class, basic_user, users):
        """ checks if method removes repeated users (by ID) """
        basic_class.users = users

        basic_class.remove_repeated_users()

        assert basic_class.users == [basic_user]

    @pytest.mark.parametrize("posts_table", ["one_post", "two_posts", "three_posts"], indirect=True)
    def test_remove_repeated_posts(self, basic_class, basic_user, basic_post, posts_table):
        """ checks if method removes repeated posts of users (by ID) """
        basic_class.users = [basic_user]
        basic_class.users[0]['posts'] = posts_table

        basic_class.remove_repeated_posts()

        assert basic_class.users[0]['posts'] == [basic_post]


pytest.main(["--verbose", "--tb=long", "test_ex2_class_pytest.py"])
