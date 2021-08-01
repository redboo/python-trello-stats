from trello_py import TrelloApi
from config import KEY, TOKEN

trello = TrelloApi(KEY, TOKEN)
board = trello.members.get_board_filter('?filter=all', 'me')
print(board)
