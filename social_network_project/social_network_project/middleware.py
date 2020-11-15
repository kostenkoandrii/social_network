from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenBackendError
from django.utils import timezone
from social_network_app.models import CustomUser


class SetUserRequestInfoMiddleware:
	"""
		Middleware that monitors users actions such as
		last login, and last request
	"""
	@staticmethod
	def decode_token(access_token):
		"""
			Method for decoding jwt token
        """
		return TokenBackend(algorithm='HS256').decode(access_token, verify=False)

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		# exclude superuser actions here
		if request.user.is_superuser:
			pass

		# monitors users login time here
		if request.path == '/auth/jwt/create/' and self.get_response(request).status_code == 200:
			if self.get_response(request).data.get('access'):
				user_id = self.decode_token(self.get_response(request).data.get('access')).get('user_id')
				CustomUser.objects.filter(id=user_id).update(last_login=timezone.now())

		# monitors users requests time here
		elif request.headers.get('Authorization'):
			try:
				user_id = self.decode_token(request.headers.get('Authorization').split(' ')[1]).get('user_id')
				CustomUser.objects.filter(id=user_id).update(last_request=timezone.now())
			except TokenBackendError as e:
				print('Token error -', e)

		return self.get_response(request)

