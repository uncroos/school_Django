from django.db import models
from django.urls import reverse
import uuid


# Genre 모델
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name


# Book 모델
class Book(models.Model):
    title = models.CharField(max_length=200)  # 책 제목
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)  # 작가 이름
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")  # 줄거리
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )  # 고유 번호 ISBN
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')  # 장르 필드

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


from django.contrib.auth.models  import User
from datetime import date
# BookInstance 모델
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique whole library')  # 고유 ID
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)  # 어떤 책의 복사본인지 연결
    imprint = models.CharField(max_length=200)  # 출판사 정보
    due_back = models.DateField(null=True, blank=True)  # 반납 기한
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # 빌린사람 추가

    # 연체 여부를 알려주는 함수
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (  # 대출 상태
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    class Meta:
        ordering = ['due_back']  # 반납 기한 순 정렬

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
#Author 모델
class Author(models.Model): #작가모델
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
