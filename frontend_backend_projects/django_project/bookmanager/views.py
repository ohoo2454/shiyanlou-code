from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BookSerializer
from .models import Book


# Create your views here.
class BookListView(APIView):

    def get(self, request, *args, **kwargs):
        all_books = Book.objects.all()
        ser_obj = BookSerializer(all_books, many=True)
        return Response(ser_obj.data)

    def post(self, request, *args, **kwargs):
        ser_obj = BookSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response(ser_obj.data)
        return Response(ser_obj.errors)


class BookView(APIView):

    def get(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.filter(pk=pk).first()
        ser_obj = BookSerializer(book_obj)
        return Response(ser_obj.data)

    def put(self, request, pk, *args, **kwargs):
        book_obj = Book.objects.filter(pk=pk).first()
        ser_obj = BookSerializer(book_obj, data=request.data, partial=True)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response(ser_obj.data)
        return Response(ser_obj.errors)

    def delete(self, request, pk, *args, **kwargs):
        obj = Book.objects.filter(pk=pk).first()
        if obj:
            obj.delete()
            return Response({'msg': '删除成功'})
        return Response({'error': '数据不存在'})
