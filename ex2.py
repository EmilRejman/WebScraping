from ex2_class import UserPostParser

# task 1:
print('TASK 1:')
users_posts_data = UserPostParser(user_url='https://jsonplaceholder.typicode.com/users',
                                  posts_url='https://jsonplaceholder.typicode.com/posts')
users_posts_data.add_users()
users_posts_data.add_posts()

# task 2:
print('TASK 2:')
number_of_posts = users_posts_data.number_of_posts_of_users()
[print(number_of_posts_of_user) for number_of_posts_of_user in number_of_posts]

# task 3:
print('TASK 3:')
users_posts_data.get_not_unique_title_list()

# task 4:
print('TASK 4:')
[users_posts_data.find_closest_user(user) for user in users_posts_data.users]
