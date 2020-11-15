import random
import string


def random_data(user=None, post=None):
	mix_list = string.ascii_letters + string.digits
	if user:
		username = ''.join((random.choice(mix_list) for i in range(random.randint(10, 15))))
		password = ''.join((random.choice(mix_list) for i in range(random.randint(10, 15))))

		return {'username': username, 'password': password}
	if post:
		title = ''.join((random.choice(mix_list) for i in range(random.randint(10, 15))))
		content = ''.join((random.choice(mix_list) for i in range(random.randint(20, 40))))
		return {'title': title, 'content': content}
