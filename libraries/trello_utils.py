from trello import TrelloClient

from trello_webhook_models import get_auth_token


class InvalidAuthToken(Exception):

    pass


def get_client():
    auth_token = get_auth_token()
    if auth_token.token is None:
        load_card('trello-token-save')
        raise InvalidAuthToken()
    return TrelloClient(api_key=shared.TRELLO_API_KEY, api_secret=shared.TRELLO_API_SECRET, token=auth_token.token)


def get_user(client):
    return client.fetch_json('/members/me')


def get_hook_url(self, base_url):
    auth_token = get_auth_token()
    return '%s?trello_api_key=%s&trello_token=%s' % (base_url, shared.TRELLO_API_KEY, auth_token.token)