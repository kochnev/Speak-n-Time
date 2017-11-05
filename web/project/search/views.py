from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F, Q
from .sql import main_search_query_text
from .forms import SearchForm
from main.models import UserProfile


@login_required
def search(request):

    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    #if len = 0 then search by default (rendering form and first auto search)
    """
    if len(request.GET) == 0:

        #is_use_intersection = 'on'
        is_use_intersection = None
        gender = None
        #берем первый изучаемый язык, в будущем добавить признак основной изучаемый
        native_language = None
        learning_language = None

        #native_language = user_profile.get_learning_languages()[0].language_id
        #learning_language = user_profile.get_native_languages()[0].language_id

        form = SearchForm({'is_use_intersection': is_use_intersection,
                           'native_language': native_language,
                           'learning_language': learning_language,
                           })
    else:
    """
    gender = request.GET.get('gender')
    is_use_intersection = request.GET.get('is_use_intersection')
    native_language = request.GET.get('native_language')
    learning_language = request.GET.get('learning_language')

    form = SearchForm(request.GET)


    if is_use_intersection == 'on':
        partners = UserProfile.objects.raw(main_search_query_text, {'userId': user.id, 'partnerId': None})
        partners_dict = dict([(p.id,p.intersection_percent) for p in partners])
        search_result = UserProfile.objects.filter(id__in = partners_dict.keys())
    else:
        partners_dict = None
        search_result = UserProfile.objects.all()

    if gender is not None and gender!='':
        search_result = search_result.filter(gender=gender)

    if native_language is not None and native_language!='':
        search_result = search_result.filter(languages=native_language,userlanguage__level='N')

    if learning_language is not None and learning_language!='':
        search_result = search_result.filter(~Q(userlanguage__level='N'),languages=learning_language)

    return render(
        request,
        'search/search_result.html',
        {
                'partners': search_result,
                'partners_dict': partners_dict,
                'form': form,
        }
        )




