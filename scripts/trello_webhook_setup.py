from trello_utils import get_client, get_user
from trello_webhook_models import TrelloBoardRequest, get_auth_token, get_user_data, get_board_request


class trello_webhook_setup(NebriOS):
    listens_to = ['trello_webhook_setup', 'child.oauth_token_setup', 'child.board_request_handled']
    required = ['trello_api_key', 'trello_api_secret', 'instance_name', 'past_due_notify_address',
                'completed_notify_address']

    # Note: This script is used to set up the trello webhook system.
    # If shared.TRELLO_API_KEY and shared.TRELLO_API_SECRET are not created,
    # you should supply them like so:
    # trello_webhook_setup := True
    # trello_api_key := <api_key>
    # trello_api_secret := <api_secret>
    # instance_name := <instance_name>
    # past_due_notify_address := <past_due_notify_address>
    # completed_notify_address := <completed_notify_address>

    def check(self):
        if child is not None:
            return child.oauth_token_setup == True or child.board_request_handled == True
        return self.trello_webhook_setup == True

    def action(self):
        if child is None:
            self.trello_webhook_setup = "Ran"
            # check for existance of callback urls
            if shared.TRELLO_WEBHOOK_MEMBER_CALLBACK_URL is None:
                shared.TRELLO_WEBHOOK_MEMBER_CALLBACK_URL = 'https://%s.nebrios.com/api/v1/trello_webhook/member_callback' \
                                                            % self.instance_name
            if shared.TRELLO_WEBHOOK_BOARD_CALLBACK_URL is None:
                shared.TRELLO_WEBHOOK_BOARD_CALLBACK_URL = 'https://%s.nebrios.com/api/v1/trello_webhook/board_callback' % \
                                                           self.instance_name
            # check for existence of trello api key
            if shared.TRELLO_API_KEY is None:
                shared.TRELLO_API_KEY = self.trello_api_key
            # check for existence of trello api secret
            if not shared.TRELLO_API_SECRET:
                shared.TRELLO_API_SECRET = self.trello_api_secret
            # check for existence of past due notification address
            if shared.PAST_DUE_NOTIFY_ADDRESS is None:
                shared.PAST_DUE_NOTIFY_ADDRESS = self.past_due_notify_address
            # check for existence of completed notification address
            if shared.COMPLETED_NOTIFY_ADDRESS is None:
                shared.COMPLETED_NOTIFY_ADDRESS = self.completed_notify_address
        # next let's see if a token exists
        auth_token = get_auth_token(PARENT=self)
        if auth_token.token is None:
            # no token yet, let's load the card.
            auth_token.trello_api_key = self.trello_api_key
            auth_token.trello_api_secret = self.trello_api_secret
            auth_token.save()
            load_card('trello-token-save', pid=auth_token.PROCESS_ID)
            return
        client = get_client()
        user = get_user(client)
        local_user_data = get_user_data(user['id'])
        if child is not None:
            if child.kind == "trelloboardrequest":
                if child.board_kind == "backup":
                    local_user_data.backup_board_id = child.board_id
                elif child.board_kind == "deleted":
                    local_user_data.deleted_list_id = child.board_id
                elif child.board_kind == "archive":
                    local_user_data.archived_list_id = child.board_id
                local_user_data.save()
        local_data_failure = False
        if local_user_data.backup_board_id is None:
            local_data_failure = True
            request, created = get_board_request("backup", PARENT=self)
            if created:
                load_card('trello-board-request', pid=request.PROCESS_ID)
        if local_user_data.deleted_list_id is None:
            local_data_failure = True
            request, created = get_board_request("deleted", PARENT=self)
            if created:
                load_card('trello-board-request', pid=request.PROCESS_ID)
        if local_user_data.archived_list_id is None:
            local_data_failure = True
            request, created = get_board_request("archive", PARENT=self)
            if created:
                load_card('trello-board-request', pid=request.PROCESS_ID)
        if not local_data_failure:
            self.completed_setup = True

