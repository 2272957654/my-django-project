from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Book
import json

@csrf_exempt
def book_list(request):
	if request.method == 'GET':
		books = list(Book.objects.values())
		return JsonResponse(books, safe=False)

@csrf_exempt
def book_detail(request, pk):
	try:
		book = Book.objects.get(pk=pk)
	except Book.DoesNotExist:
		return HttpResponseNotFound('Book not found')
	if request.method == 'GET':
		return JsonResponse({
			'id': book.id,
			'title': book.title,
			'author': book.author,
			'published_date': book.published_date,
			'isbn': book.isbn,
			'price': str(book.price)
		})

@csrf_exempt
def book_create(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		book = Book.objects.create(**data)
		return JsonResponse({'id': book.id})

@csrf_exempt
def book_update(request, pk):
	try:
		book = Book.objects.get(pk=pk)
	except Book.DoesNotExist:
		return HttpResponseNotFound('Book not found')
	if request.method == 'POST':
		data = json.loads(request.body)
		for key, value in data.items():
			setattr(book, key, value)
		book.save()
		return JsonResponse({'id': book.id})

@csrf_exempt
def book_delete(request, pk):
	try:
		book = Book.objects.get(pk=pk)
	except Book.DoesNotExist:
		return HttpResponseNotFound('Book not found')
	if request.method == 'POST':
		book.delete()
		return JsonResponse({'result': 'deleted'})
