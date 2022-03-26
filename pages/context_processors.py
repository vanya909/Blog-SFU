import datetime as dt


def current_year_processor(request):
    return {
        'year': dt.datetime.now().year
    }
