from nebriosmodels import NebriOSModel, NebriOSField


class TrelloOAuthToken(NebriOSModel):

    token = NebriOSField(required=True, default=None)
    continue_trello_setup = NebriOSField(default=False)


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


def get_auth_token(PARENT=None):
    try:
        return TrelloOAuthToken.get()
    except Process.DoesNotExist:
        return TrelloOAuthToken(PARENT=PARENT)


def get_user_data(user_id, PARENT=None):
    try:
        return TrelloMemberData.get(user_id=user_id)
    except Process.DoesNotExist:
        member_data = TrelloMemberData(user_id=user_id, PARENT=PARENT)
        member_data.save()
        return member_data