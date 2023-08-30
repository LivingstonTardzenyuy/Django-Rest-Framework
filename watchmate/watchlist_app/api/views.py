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
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# class ReviewList(generics.ListAPIView):
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]


# class UserReview(generics.ListAPIView):
#     serializer_class = ReviewSerializer   

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username = username)

    # def get_queryset(self):
    #     username = self.request.query_params.get('username', None)
    #     return Review.objects.filter(review_user__username = username)


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.GET.get('username')
        return Review.objects.filter(review_user__username=username)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes =  [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']


    def get_queryset(request):
        return Review.objects.all()
    
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_querryset = Review.objects.filter(watchlist = watchlist, review_user = review_user)

        if review_querryset.exists():
            raise ValidationError("You have already reviewed this movie")
        
        if watchlist.number_ratings == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        
        watchlist.number_rating +=1

        serializer.save(watchlist = watchlist, review_user = review_user)
        # return Response(serializer_review.datavc

    # def post(self, request):
    #     serializer_review = ReviewSerializer(data = request.data)

    #     review_user = self.request.user
    #     watchlist = WatchList.object.get(pk=pk) 
    #     review_queryset = Review.objects.filter(watchlist = watchlist, review_user = review_user)

    #     if review_queryset.exists():
    #         raise ValidationEror("You have already reviewed This WatchLIst")

    #     if serializer_review.is_valid():
    #         serializer_review.save(watchlist = watchlist, review_user = review_user)
    #         return Response(serializer_review.data)
    #     else:
    #         return Response(serializer_review.errors)
    def post(self, request, pk):
        serializer_review = ReviewSerializer(data=request.data)

        review_user = self.request.user
        watchlist = WatchList.objects.get(pk=pk)  # Retrieve the watchlist using pk parameter

        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this WatchList")

        if serializer_review.is_valid():
            serializer_review.save(watchlist=watchlist, review_user=review_user)

            # Update watchlist average rating and number of ratings
            if watchlist.number_rating == 0:
                watchlist.avg_rating = serializer_review.validated_data['rating']
            else:
                total_rating = watchlist.avg_rating * watchlist.number_ratings
                total_rating += serializer_review.validated_data['rating']
                watchlist.avg_rating = total_rating / (watchlist.number_ratings + 1)
            watchlist.number_ratings += 1
            watchlist.save()

            return Response(serializer_review.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_review.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetails(APIView):
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]



    def get(self, request, pk):
        try:
            review = Review.objects.get(pk = pk)
        except Review.DoesNotExist:
            return Response({'Error: Stream does not exist'}, status = status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, many = False)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            review = Review.objects.get(pk = pk)
        
        except Review.DoesNotExist:
            return Response({'Error: Stream does not exist'}, status = status.HTTP_404_NOT_FOUND)

        if review.review_user != request.user:
            return Response({'Error: You are not Authorize to perfom this request'}, status=status.HTTP_403_FORBIDDEN)

        
        serializer = ReviewSerializer(review, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


    def delete(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        return Response(status= status.HTTP_201_OK)


class StreamPlatFormList(APIView):

    permission_classes = [IsAdminOrReadOnly]

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

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']


class WatchListList(APIView):

    permission_classes = [IsAdminOrReadOnly]
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


    permission_classes = [IsAdminOrReadOnly]

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

        


