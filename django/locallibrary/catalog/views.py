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

# 빌린 책 목록을 불러오기
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm
import datetime

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # POST 요청이 들어오면 갱신처리 시작
    if request.method == 'POST':
        # form 인스턴스를 만들고 요청한 정보로 데이터를 채움
        form = RenewBookForm(request.POST)

        # 폼 유효성 검사
        if form.is_valid():
            # form.cleaned_data 데이터를 요청 받은대로 처리
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

    # GET이나 다른 요청 들어오면 default form 사용
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
