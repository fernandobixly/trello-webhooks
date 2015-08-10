from nebriosmodels import NebriOSModel, NebriOSField


class TrelloOAuthToken(NebriOSModel):

    token = NebriOSField(default=None)
    trello_api_key = NebriOSField(default=None)
    trello_api_secret = NebriOSField(default=None)
    oauth_token_setup = NebriOSField(default=False)


class TrelloMemberData(NebriOSModel):

    user_id = NebriOSField(required=True)
    backup_board_name = NebriOSField()
    backup_board_id = NebriOSField()
    deleted_list_name = NebriOSField()
    deleted_list_id = NebriOSField()
    archived_list_name = NebriOSField()
    archived_list_id = NebriOSField()


class TrelloBoardRequest(NebriOSModel):

    board_kind = NebriOSField(required=True)
    board_url = NebriOSField()
    board_id = NebriOSField(default=None)
    board_request_handled = NebriOSField(default=False)


def get_auth_token(PARENT=None):
    try:
        return TrelloOAuthToken.get()
    except Process.DoesNotExist:
        oauthtoken = TrelloOAuthToken(PARENT=PARENT)
        oauthtoken.save()
        return oauthtoken


def get_user_data(user_id, PARENT=None):
    try:
        return TrelloMemberData.get(user_id=user_id)
    except Process.DoesNotExist:
        member_data = TrelloMemberData(user_id=user_id, PARENT=PARENT)
        member_data.save()
        return member_data


def get_board_request(board_kind, PARENT=None):
    try:
        return TrelloBoardRequest.get(board_kind=board_kind), False
    except:
        board_request = TrelloBoardRequest(board_kind=board_kind, PARENT=PARENT)
        board_request.save()
        return board_request, True