from typing import Any, Dict, List, Union

import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Requests


def get_response(request: Any) -> List[Dict[str, int]]:
    """
    Get request if questions_num > 1.
    """

    url: str = 'https://jservice.io/api/random?count='
    request_: int = request.data.get('questions_num', 1)
    return requests.get(
        f'{url}{request_}').json()


def get_context() -> Union[dict, str]:
    answer = Requests.objects.last()
    if answer is None:
        return {
            "info": "Send POST requests: {'questions_num': 1}"}
    return {
        'id': answer.id_req,
        'question': answer.text_question,
        'answer': answer.text_answer,
        'created': answer.created_at,
    }


@api_view(['post', 'get'])
def get_questions(request: Any) -> Any:
    """
    Send POST requests: {"questions_num": integer}
    Example: {"questions_num": 1}
    Maximum number 1 or <= 100
    """

    request_: Union[int, None] = request.data.get('questions_num')

    if request_ is None:
        return Response(
            get_context(),
            status=status.HTTP_204_NO_CONTENT)
    if request_ not in range(1, 101):
        return Response(
            {'error': 'questions_num < 1 or questions_num > 100'},
            status=status.HTTP_204_NO_CONTENT)
    if request_:
        for items in get_response(request):
            try:
                text_question = items.get('question'),
            except AttributeError:
                return Response(
                    {'error': 'questions_num < 1'},
                    status=status.HTTP_204_NO_CONTENT)
            if Requests.objects.filter(
                    text_question=text_question[0]).exists():
                items = get_unique(request)
            Requests.objects.create(
                id_req=items.get('id'),
                text_answer=items.get('answer'),
                text_question=items.get('question'),
                created_at=items.get('created_at'))
        return Response(
            get_context(),
            status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'question': ''},
        status=status.HTTP_204_NO_CONTENT)


def get_unique(request: Any) -> Dict[str, int]:
    """
    Get a unique question from endpoint
    https://jservice.io/api/random?count=1
    """

    for items in get_response(request):
        text_question = items.get('question'),
        if Requests.objects.select_related('text_question').filter(
                text_question=text_question[0]
        ).exists():
            items = get_unique(request)
    return items
