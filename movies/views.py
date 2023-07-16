from django.shortcuts import render
from rest_framework.views import APIView, Request, Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from movies.permissions import AuthenticatedMovie, IsEmployee
from movies.serializers import MovieSerializer, OrderMovieSerializer
from django.shortcuts import get_object_or_404
from .models import Movie
import ipdb
from rest_framework.pagination import PageNumberPagination

class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployee]

    pagination_class = PageNumberPagination
    pagination_class.page_size = 2 

    def get(self, request: Request) -> Response:
        users = Movie.objects.all().order_by('id')
        result_page = self.paginate_queryset(users, request, self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)
        return Response(serializer.data, 201)


class OrderMovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = OrderMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(movie=movie, user=request.user)

        return Response(serializer.data, 201)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployee]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=204)
