from trello import TrelloApi
from config import BOARD_ID, KEY, TOKEN
from period import Period

trello = TrelloApi(KEY, TOKEN)

# Get filtered members
users = trello.boards.get_membership(
    BOARD_ID, filter='normal', member='true', member_fields='fullName')
board_users = {}
for user in users:
    board_users[user['idMember']] = user['member']['fullName']


# Get actions
action_users = []
limit = 1000
page = 0
count = 0
# period < day | week | month | year >
period = Period().get('year')
if period:
    since, before = period
    print(since, before)

    while True:
        actions = trello.boards.get_action(
            BOARD_ID,
            filter="all",
            limit=limit,
            since=since,
            before=before,
            page=page,
            fields='idMemberCreator,type,date',
            memberCreator='false',
            member='false')
        count += len(actions)

        [action_users.append(action['idMemberCreator']) for action in actions]

        if actions and len(actions) == limit:
            page += 1
            continue
        else:
            break

    print("total actions:", count)
    action_users = set(action_users)

    [board_users.pop(active, None) for active in action_users]

    if board_users:
        print("Users to be removed: ", board_users)
        confirm = input("Remove users [y/n]: ")
        if 'y' == confirm.lower():
            print("Remove started:")
            for id in list(board_users.keys()):
                trello.boards.delete_member_idMember(id, BOARD_ID)
                print(
                    f"User {id} aka '{board_users[id]}' remotely successfully")
        else:
            print('Deletion canceled.')
    else:
        print('Nobody to delete.')
