from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('', include(('misc.urls', 'misc'), namespace='misc')),
    path('authorization/', include(('authorization.urls', 'authorization'), namespace='authorization')),
    path('courses/', include(('course.urls', 'course'), namespace='course')),
]

handler400 = 'misc.views.handle_page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

