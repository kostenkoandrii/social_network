import random
import string


def random_data(user=None, post=None):
	"""
		Universal method for making random user data such as username and password
		and random post data such as title and content

       :param user: if user=True, method return user data
       :param post: if post=True, method return post data
       :return: random user data or post data
    """
	mix_list = string.ascii_letters + string.digits
	if user:
		username = ''.join((random.choice(mix_list) for i in range(random.randint(10, 15))))
		password = ''.join((random.choice(mix_list) for i in range(random.randint(10, 15))))

		return {'username': username, 'password': password}
	if post:
		title = ''.join((random.choice(mix_list) for i in range(random.randint(10, 15))))
		content = ''.join((random.choice(mix_list) for i in range(random.randint(20, 40))))
		return {'title': title, 'content': content}
