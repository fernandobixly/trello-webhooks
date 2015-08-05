from trello import TrelloClient

from trello_webhook_models import get_auth_token


class InvalidAuthToken(Exception):

    pass


def get_client():
    auth_token = get_auth_token()
    if auth_token.token is None:
        raise InvalidAuthToken()
    return TrelloClient(api_key=shared.TRELLO_API_KEY, api_secret=shared.TRELLO_API_SECRET, token=auth_token.token)