from django.contrib import admin

# 관리 페이지에 등록할 모델(?)
# 이 모델들은 catalog 애플리케이션에 정의되어 있습니다.
from catalog.models import Author, Genre, Book, BookInstance

# 4개의 모델을 admin 페이지에 등록?할거임
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)