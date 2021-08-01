import requests
from config import KEY, TOKEN


def create_board(board_name):
    url = "https://api.trello.com/1/boards/"
    querystring = {"name": board_name, "key": KEY, "token": TOKEN}
    response = requests.request("POST", url, params=querystring)
    board_id = response.json()["shortUrl"].split("/")[-1].strip()
    return board_id


def list_boards(board_filter="all"):
    url = f"https://api.trello.com/1/members/me/boards/?filter={board_filter}"
    querystring = {"key": KEY, "token": TOKEN}
    headers = {}
    headers['Accept'] = 'application/json'
    response = requests.request(
        "GET", url, params=querystring, headers=headers)
    boards = response.json()
    for board in boards:
        print(board["name"], board['id'])


list_boards()
