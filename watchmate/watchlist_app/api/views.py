from rest_framework.response import Response
from watchlist_app.models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework import mixins
from rest_framework.exceptions import ValidationError



class ReviewList(APIView):
    
    def get(self,request):
        review = Review.objects.all()
        serializer_review = ReviewSerializer(review, many = True)
        return Response(serializer_review.data)

    def post(self, request):
        serializer_review = ReviewSerializer(data = request.data)

        review_user = self.request.user 
        review_queryset = Review.objects.filter(watchlist = watchlist, review_user = review_user)

        if review_queryset.exists():
            raise ValidationEror("You have already reviewed This WatchLIst")

        if serializer_review.is_valid():
            serializer_review.save()
            return Response(serializer_review.data)
        else:
            return Response(serializer_review.errors)
           
class ReviewDetails(APIView):
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk = pk)
        except Review.DoesNotExist:
            return Response({'Error: Stream does not exist'}, status = status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, many = False)
        return Response(serializer.data)
class StreamPlatFormList(APIView):
    def get(self, request):
        stream = StreamPlatForm.objects.all()
        serializer = StreamPlatFormSerializer(stream, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatFormSerializer(data = request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
        else:
            return Response(serializer.errors)
        

class StreamPlatFormDetails(APIView):
    def get(self, request, pk):
        try:
            stream = StreamPlatForm.objects.get(pk= pk)
        except StreamPlatForm.DoesNotExist:
            return Response({'Error: Stream does not exist'}, status = status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatFormSerializer(stream, many = False)
        return Response(serializer.data)

    def put(self, request, pk):
        stream = StreamPlatForm.objects.get(pk = pk)
        serializer = StreamPlatFormSerializer(stream, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        stream = StreamPlatForm.objects.get(pk = pk)
        stream.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class WatchListList(APIView):
    def get(self, request):
        movie = WatchList.objects.all()
        serializer = WatchListSerializer(movie, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
           return Response(serializer.errors)

class WatchListDetails(APIView):
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk = pk)
        except Movie.DoesNotExist:
            return Response({'error' : 'Movie not found'}, status = status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie, many = False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk = pk)
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk = pk)
        movie.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

        



# @api_view(['GET', 'POST'])
# def movie_list(request): 
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many = True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk = pk)
        
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'}, status = status.HTTP_404_NOT_FOUND
        
#         serializer = MovieSerializer(movie, many = False)
#         return Response(serializer.data)

#     if request.method == 'PUT':

#         movie = Movie.objects.get(pk=pk)
        
#         serializer = MovieSerializer(movie, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         else:
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk = pk)
#         movie.delete()
#         return Response(status = HTTP_200_NO_CONTENT)