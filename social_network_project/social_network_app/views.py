from django.core.exceptions import ValidationError
from django.utils.datetime_safe import date
from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from .models import SimplePost, Like, CustomUser
from .permissions import IsOwner, IsUserOwner
from .serializers import SimplePostSerializer, LikeSerializer, UserActivitySerializer


class SimplePostViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin,
						mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
	"""
		Controller for users post model.
		User can do actions with post such as:
		create, update, delete, get list of posts, get selected post
	"""
	permission_classes = [IsAuthenticated, IsOwner]
	serializer_class = SimplePostSerializer

	def get_queryset(self):
		user = self.request.user
		return SimplePost.objects.filter(author=user)

	def perform_create(self, serializer):
		user = self.request.user
		serializer.save(author=user)


class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
	"""
		Controller for post likes.
		User can create like for selected post
		and delete likes witch was created be his self
	"""
	permission_classes = [IsAuthenticated, IsOwner]
	serializer_class = LikeSerializer
	queryset = Like.objects.all()

	def create(self, request, *args, **kwargs):

		request.data._mutable = True
		request.data.update({'author': self.request.user.id})
		request.data._mutable = False

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)

		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeAnalyticsViewSet(mixins.ListModelMixin, GenericViewSet):
	"""
		Controller for get analytics about posts likes:
		User can get the number of likes given to his posts
		in selected period.
		date format: [YYYY-MM-DD]
	"""
	permission_classes = [IsAuthenticated, IsOwner]

	def list(self, request, *args, **kwargs):
		queryset = Like.objects.filter(post__author=self.request.user)
		if queryset:
			date_from = request.query_params.get(
				'date_from', queryset.order_by('created').first().created)
			date_to = request.query_params.get('date_to', date.today())
			try:
				data = [{
					'count_likes': queryset.filter(
						created__gte=date_from,
						created__lte=date_to).count()
				}]
			except ValidationError:
				return Response(data=['Date is not valid'], status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response(data)
		else:
			return Response([{'count_likes': 0}])


class UserActivityViewSet(mixins.RetrieveModelMixin, GenericViewSet):
	"""
		Simple controller for get data about user such as
		last login, last request at application
	"""
	permission_classes = [IsAuthenticated, IsUserOwner]
	serializer_class = UserActivitySerializer
	queryset = CustomUser.objects.all()
