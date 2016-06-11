# from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_api.speech.serializers import CreateUserSerializer, SpeechInputSerializer
from nlp import findSVOs

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows user to be viewed and edited.
	"""
	# queryset = User.objects.all().order_by('-date_joined')

	serializer_class = CreateUserSerializer

	def get_queryset(self):
		if self.request.user.is_superuser:
			return User.objects.all()
		else:
			return User.objects.filter(id=self.request.user.id)

	def get_permissions(self):
	       # Your logic should be all here
	       if self.request.method == 'POST':
	           self.permission_classes = (AllowAny, )
	       else:
	           self.permission_classes = (IsAuthenticated, )

	       return super(UserViewSet, self).get_permissions()	

# class GroupViewSet(viewsets.ModelViewSet):
# 	"""
# 	API endpoint that allows groups to be viewed and edited.
# 	"""
# 	queryset = Group.objects.all()
# 	serializer_class = GroupSerializer

class SpeechView(views.APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		# Validate incoming input
		serializer = SpeechInputSerializer(data = request.query_params)
		serializer.is_valid(raise_exception = True)
		# Get model input
		data = serializer.validated_data
		transcript = data["transcript"]
		# Perform calculations
		result = findSVOs(transcript)
		# Return result in custom format
		return Response({
				"input": transcript,
				"result": result,
			})