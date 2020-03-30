import pytest
from app import ex2_class


@pytest.fixture(scope="function", name="basic_class", autouse=True)
def fixture_basic_class():
    return ex2_class.UserPostParser()


@pytest.fixture(scope="function", name="basic_user")
def fixture_basic_user(request):
    user = dict(id=1, name='Leanne Graham', username='Bret', email='Sincere@april.biz',
                address=dict(street='Kulas Light', suite='Apt. 556', city='Gwenborough',
                             zipcode='92998-3874', geo={'lat': -37.3159, 'lng': 81.1496}),
                phone='1-770-736-8031 x56442', website='hildegard.org',
                company=dict(name='Romaguera-Crona',
                             catchPhrase='Multi-layered client-server neural-net',
                             bs='harness real-time e-markets'), posts=[])  # , posts=[]
    return user


@pytest.fixture(scope="function", name="basic_post")
def fixture_basic_post():
    post = dict(userId=1, id=1,
                title="sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                body="quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto")

    return post


@pytest.fixture(name="group")
def fixture_group(request, basic_user, basic_class, basic_post):  # the fixture inherits other fixtures from fixture
    group_name = request.param  # this is argument passed from @pytest.mark.parametrize in next test function, thats why it has acces through  indirect=True
    groups = {
        #patter: class, users, posts
        "no_users": [basic_class, [], [basic_post] ],
        "no_posts": [basic_class, [basic_user], []],
        "posts_None": [basic_class, [basic_user], None],
    }
    return groups[group_name]  # zwracamy returna od group_name

@pytest.fixture(name="posts_table")
def fixture_posts_table(request, basic_post):
    group_name = request.param
    groups = {
        #patter: class, users, posts
        "one_post": [basic_post],
        "two_posts": [basic_post,basic_post],
        "three_posts": [basic_post, basic_post, basic_post],
    }
    return groups[group_name]

@pytest.fixture(name="result")
def fixture_result(request, basic_post):
    group_name = request.param
    groups = {
        #patter: class, users, posts
        "none": [],
        "post": [basic_post['title']],
    }
    return groups[group_name]


@pytest.fixture(name="users")
def fixture_users(request, basic_user):
    group_name = request.param
    groups = {
        #patter: class, users, posts
        "single_user": [basic_user],
        "many_users": [basic_user,basic_user]
    }
    return groups[group_name]