from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import FAQ
from .serializers import FAQSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['question', 'answer']

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset, 
            many=True, 
            context={'lang': lang}
        )
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = FAQ.objects.all()
        # Add created_at filter
        created_after = self.request.query_params.get('created_after', None)
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)
        return queryset

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset, 
            many=True, 
            context={'lang': lang}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def languages(self, request):
        """Return available languages"""
        return Response({
            'languages': [
                {'code': 'en', 'name': 'English'},
                {'code': 'hi', 'name': 'Hindi'},
                {'code': 'bn', 'name': 'Bengali'}
            ]
        })