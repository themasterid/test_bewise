import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Requests


def get_response(request):
    """
    Get request if questions_num > 1.
    """

    request_ = request.data.get('questions_num', 1)
    response = requests.get(
        f'https://jservice.io/api/random?count={request_}')
    return response.json()


@api_view(['post', 'get'])
def get_questions(request):
    """
    Send POST requests on endpoint
    https://jservice.io/api/random?count=1<br>
    Content: {"questions_num": integer}<br>
    Example: {"questions_num": 2}
    """

    request_ = request.data.get('questions_num')
    if request_ is None:
        return Response(
                    {'question': f'{Requests.objects.all().last()}'},
                    status=status.HTTP_204_NO_CONTENT)
    if request_:
        text_ = get_response(request)
        for items in text_:
            text_question = items.get('question'),
            if Requests.objects.filter(
                    text_question=text_question[0]).exists():
                items = get_unique(request)
            Requests.objects.create(
                id_req=items.get('id'),
                text_answer=items.get('answer'),
                text_question=items.get('question'),
                created_at=items.get('created_at'))
        return Response(
                    {'question': f'{Requests.objects.all().last()}'},
                    status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'question': ''},
        status=status.HTTP_204_NO_CONTENT)


def get_unique(request):
    """
    Get a unique question from endpoint
    https://jservice.io/api/random?count=1
    """

    for items in get_response(request):
        text_question = items.get('question'),
        if Requests.objects.filter(
                text_question=text_question[0]).exists():
            items = get_unique(request)
    return items
