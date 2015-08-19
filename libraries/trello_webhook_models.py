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


class TrelloBoard(NebriOSModel):

    board_id = NebriOSField(required=True)
    board_name = NebriOSField(required=True)
    board_hook_setup = NebriOSField(required=True, default=False)

    @classmethod
    def from_trello_board(cls, board):
        trello_board = None
        try:
            trello_board = TrelloBoard.get(board_id=board.id)
        except Process.DoesNotExist:
            trello_board = TrelloBoard(board_id=board.id)
        trello_board.board_name = board.name
        trello_board.save()
        for list_obj in board.all_lists():
            TrelloList.from_trello_list(trello_board, list_obj)
        return trello_board


class TrelloList(NebriOSModel):

    list_id = NebriOSField(required=True)
    list_name = NebriOSField(required=True)

    @classmethod
    def from_trello_list(cls, trello_board, list_obj):
        trello_list = None
        try:
            trello_list = TrelloList.get(list_id=list_obj.id)
        except Process.DoesNotExist:
            trello_list = TrelloList(list_id=list_obj.id, PARENT=trello_board)
        trello_list.list_name = list_obj.name
        trello_list.save()
        for card in list_obj.list_cards():
            TrelloCard.from_trello_card(trello_list, card)
        return trello_list


class TrelloCard(NebriOSModel):

    card_id = NebriOSField(required=True)
    card_name = NebriOSField(required=True)
    card_short_link = NebriOSField()
    card_member_creator = NebriOSField()
    card_moved = NebriOSField(default=False)
    card_closed = NebriOSField(default=False)
    card_closed_datetime = NebriOSField()
    card_closed_date = NebriOSField()
    card_closed_by_noncreator = NebriOSField(default=False)
    card_deleted = NebriOSField(default=False)
    card_deleted_datetime = NebriOSField()
    card_deleted_date = NebriOSField()
    card_deleted_by_noncreator = NebriOSField(default=False)
    card_archived = NebriOSField(default=False)
    card_archived_datetime = NebriOSField()
    card_archived_date = NebriOSField()
    card_archived_by_noncreator = NebriOSField(default=False)
    card_due = NebriOSField()
    card_due_date = NebriOSField()
    card_is_due = NebriOSField(default=False)
    card_json = NebriOSField()

    @classmethod
    def from_trello_card(cls, trello_list, card):
        trello_card = None
        try:
            trello_card = TrelloCard.get(card_id=card.id)
        except Process.DoesNotExist:
            trello_card = TrelloCard(card_id=card.id, PARENT=trello_list)
        trello_card.card_name = card.name
        trello_card.save()
        return trello_card


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