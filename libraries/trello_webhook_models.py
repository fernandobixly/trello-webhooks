from nebriosmodels import NebriOSModel, NebriOSField


class OAuthToken(NebriOSModel):

    token = NebriOSField(required=True, default=None)


class TrelloMemberData(NebriOSModel):

    member_id = NebriOSField(required=True)
    backup_board_name = NebriOSField()
    backup_board_id = NebriOSField()
    deleted_list_name = NebriOSField()
    deleted_list_id = NebriOSField()
    archived_list_name = NebriOSField()
    archived_list_id = NebriOSField()


def get_auth_token():
    try:
        return OAuthToken.get()
    except Process.DoesNotExist:
        return OAuthToken()