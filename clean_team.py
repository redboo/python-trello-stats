'''Clean inactive memberships from an organization.'''
from datetime import datetime, timedelta
from trello import TrelloApi
from config import KEY, TOKEN
from requests.models import HTTPError


class CleanTeam:

    def __init__(self, organization_id: str) -> None:
        self.trello = TrelloApi(KEY, TOKEN)
        self.organization_id = organization_id

    def mongo_date(self, id: str) -> datetime:
        '''Get date from mongoID object.'''
        return datetime.fromtimestamp(int(id[:8], 16))

    def get_inactive_members_of_org(self, days: int) -> dict:
        '''Get inactive memberships of an organization.'''
        print(f"Getting inactive members of organization for {days} days…")

        self.before = datetime.utcnow()
        self.since = self.before - timedelta(days=days)

        # get all memberships of an organization
        all_memberships = self.trello.organizations.get_membership(
            self.organization_id, filter='all', member='true')
        if not all_memberships:
            raise Exception("No memberships")

        # get added memberships to an organization before date
        members_before = {mem['member']['id']: '@' + mem['member']['username']
                          for mem in all_memberships if self.mongo_date(mem['id']) < self.since}
        if not members_before:
            raise Exception(f"No memberships before {str(self.since)[:10]}")

        # get all boards of an organization
        boards = self.trello.organizations.get_board(self.organization_id)
        if not boards:
            raise Exception("No boards of an organization")
        all_boards = {board['id']: board['name']
                      for board in boards if board['name'] != 'z[Unused board]'}

        # get active members of an organization
        active_members = self.get_active_members(all_boards)

        # get list of inactive memberships of an organization
        [members_before.pop(active, None) for active in active_members]

        return members_before

    def get_active_members(self, boards: str) -> set:
        '''Get active members of boards.'''
        active_members = []
        limit = 1000

        for board_id in boards:
            page = 1
            before = self.before
            while True:
                actions = self.trello.boards.get_action(
                    board_id,
                    limit=limit,
                    since=self.since,
                    before=before,
                    fields='idMemberCreator,date',
                    memberCreator='false',
                    member='false')

                if actions:
                    [active_members.append(action['idMemberCreator'])
                     for action in actions]
                if actions and len(actions) == limit:
                    before = actions[-1]['date']
                    page += 1
                    continue
                else:
                    break

        return set(active_members)

    def post_comment(self, users: dict, card_output_id: str) -> None:
        '''Post comment with a inactive users list to a card.'''
        if users:
            len(users)
            text = f"{len(users)} users may be removed as inactive since *{str(self.since)[:10]}*: "
            text += ' '.join(users.values())

            try:
                self.trello.cards.new_action_comment(card_output_id, text)
                print(text)
            except HTTPError as e:
                print(e)
        else:
            print('List of users is empty. Comment not created.')

# Example
# org = CleanTeam('thevenusproject1')
# inactive_members = org.get_inactive_members_of_org(days=180)
# if inactive_members:
#     org.post_comment(inactive_members, 'uWtbF23I')
# else:
#     print('No inactive memberships.')
