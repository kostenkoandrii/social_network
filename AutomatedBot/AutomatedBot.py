from time import sleep

import requests
from DataGenerator import random_data
from configs import configs
import ast
import random

host = "http://127.0.0.1:8000/"

like_create_url = 'api/like/'
post_create_url = 'api/post/'
login_url = 'auth/jwt/create/'
register_url = 'auth/users/'

users_credentials = {}
login_credentials = {}
posts = []


def request_maker(url, headers=None, data=None, method=None):
	"""
		Universal method for sending requests. At now have only post method,
		but can include other in the future

	   :param url: Request url
       :param headers: Request headers
       :param data: Request data
       :param method: Request method
       :return: Http Response
    """
	if method == 'post':
		return requests.post(url=host+url, headers=headers, data=data)


def register_users(number_of_users):
	"""
		Method for register users with random data
		:param number_of_users: maximal number of users witch need to be registered
	"""
	for reg in range(number_of_users):
		user_data = random_data(user=True)
		response = request_maker(url=register_url, data=user_data, method='post')
		if response.status_code == 201:
			user_data['id'] = ast.literal_eval(response.text).get('id')
			users_credentials[f'user{reg+1}'] = user_data
			print(f'User with username - {user_data.get("username")} was Success register')


def login_users():
	"""
		Method for login registered users
	"""
	for user, data in users_credentials.items():
		data = {
			'username': data.get('username'),
			'password': data.get('password')
		}
		response = request_maker(url=login_url, data=data, method='post')
		if response.status_code == 200:
			token = f'Bearer {ast.literal_eval(response.text).get("access")}'
			login_credentials[user] = data
			login_credentials[user]['token'] = token
			print(f"User - {data.get('username')}, Success Login")


def user_post_create(max_posts_per_user):
	"""
		Method for register users with random data
		:param max_posts_per_user: maximal number of post witch user need create
	"""
	for data in login_credentials.values():
		post_data = random_data(post=True)
		headers = {'Authorization': data.get('token')}

		for action in range(random.randint(1, max_posts_per_user)):
			response = request_maker(url=post_create_url, headers=headers, data=post_data, method='post')
			if response.status_code == 201:
				posts.append(ast.literal_eval(response.text))
				print(f'User {data.get("username")} create Post - {response.text}')


def user_post_like(max_likes_per_user):
	"""
		Method for making likes to the posts, made by user
		:param max_likes_per_user: maximal number of likes witch user need to make
	"""
	if max_likes_per_user <= len(posts):
		for user_data in login_credentials.values():
			random_likes_action_count = random.randint(1, max_likes_per_user)
			counter = 0
			headers = {'Authorization': user_data.get('token')}

			while random_likes_action_count != counter:
				post_index = random.randint(0, len(posts) - 1)
				post_id = posts[post_index].get('id')
				data = {'post': post_id}

				response = request_maker(url=like_create_url, headers=headers, data=data, method='post')

				if response.status_code == 201:
					counter += 1
					print(f"User {user_data.get('username')} has like post with id - {post_id}")
				else:
					continue
	else:
		print('User can not make more Likes then Posts exist')


print('START REGISTRATION')
sleep(2)
register_users(configs.get('number_of_users'))
print()

print('START LOGIN')
sleep(2)
login_users()
print()

print('START POST CREATING')
sleep(2)
user_post_create(configs.get('max_posts_per_user'))
print()

print('START POST LIKING')
sleep(2)
user_post_like(configs.get('max_likes_per_user'))