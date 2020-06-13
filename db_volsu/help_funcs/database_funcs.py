from collections import namedtuple

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_context(request, connection, sql_raw):
    with connection.cursor() as cursor:
        cursor.execute(sql_raw)
        result = namedtuplefetchall(cursor)

    paginator = Paginator(result, 2)
    page_number = request.GET.get('page')

    try:
        page_result = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_result = paginator.get_page(1)
    except EmptyPage:
        page_result = paginator.get_page(paginator.num_pages)

    return page_result
