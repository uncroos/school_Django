from django.shortcuts import render

from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    num_books = Book.objects.all().count() # 책 오브젝트를 모두 가져오고 갯수를 카운트
    num_instances = BookInstance.objects.all().count() # 책복사본 오브젝트를 다 가져오고 갯수를 카운트
    
    # 대출 가능한 책의 갯수를 카운트.
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # 작가를 모두 가져오고 갯수를 카운트
    num_authors = Author.objects.count()

    # session을 사용해서 방문자수 받아오기
    num_visit = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visit + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits' : num_visit,
    }

    # index.html에 변수를 render한다.
    return render(request, 'index.html', context=context)


from django.views import generic

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book