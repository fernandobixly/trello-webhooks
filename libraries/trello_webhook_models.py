from nebriosmodels import NebriOSModel, NebriOSField


class TrelloOAuthToken(NebriOSModel):

    token = NebriOSField(required=True, default=None)


class TrelloMemberData(NebriOSModel):

    user_id = NebriOSField(required=True)
    backup_board_name = NebriOSField()
    backup_board_id = NebriOSField()
    deleted_list_name = NebriOSField()
    deleted_list_id = NebriOSField()
    archived_list_name = NebriOSField()
    archived_list_id = NebriOSField()


def get_auth_token():
    try:
        return TrelloOAuthToken.get()
    except Process.DoesNotExist:
        return TrelloOAuthToken()


def get_member_data(user_id):
    try:
        return TrelloMemberData.get(user_id=user_id)
    except Process.DoesNotExist:
        member_data = TrelloMemberData(user_id=user_id)
        member_data.save()
        return member_data