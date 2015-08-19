from trello_utils import get_client, get_hook_url


class trello_board_hook_setup(NebriOS):
    listens_to = ['board_hook_setup']

    def check(self):
        return self.board_hook_setup == False

    def action(self):
        client = get_client()
        client.create_hook(get_hook_url(shared.TRELLO_WEBHOOK_BOARD_CALLBACK_URL), self.board_id)
        self.board_hook_setup = True