from fastapi.testclient import TestClient
from constantVariables import *
from dbconnection import DataBase
import pytest
import random

from main import app

client = TestClient(app)


@pytest.fixture(scope='session')
def get_all_book_titles():
    db = DataBase()
    sql = 'SELECT json_agg(title) as title_list FROM book;'
    db._cur.execute(sql)
    info = db._cur.fetchone()['title_list']
    db.db_close()
    return info

@pytest.fixture(scope='session')
def get_new_book_detail(get_all_book_titles):
    
    while True:
        ind = random.randint(0,100)
        title = f'title_{ind}'
        if get_all_book_titles and title not in get_all_book_titles:
            break
    
    return {
                "title": title,
                "author": f"author_{random.randint(10,15)}",
                "publication_year": random.randint(2000,2024)
                }

@pytest.fixture(scope='session')
def get_new_book_id(get_new_book_detail):
    
    db = DataBase()
    sql = 'SELECT book_id FROM book WHERE title = %s;'
    db._cur.execute(sql, [get_new_book_detail['title']])
    info = db._cur.fetchone()['book_id']
    db.db_close()
    return info


@pytest.fixture(scope='session')
def get_new_nonExcitant_book_id():
    
    db = DataBase()
    sql = 'SELECT json_agg(book_id) as bookid_list FROM book;'
    db._cur.execute(sql)
    bookID_list = db._cur.fetchone()['bookid_list']
    db.db_close()

    while True:
        ind = random.randint(500,1000)
        if bookID_list and ind not in bookID_list:
            break

    return ind




def test_add_book(get_new_book_detail):
    response = client.post(
        "/add-book/",
        json=get_new_book_detail,
    )
    assert response.status_code == 200
    assert response.json() == BOOK_ADDED_SUCCESSFULLY


def test_add_existing_book(get_new_book_detail):
    response = client.post(
        "/add-book/",
        json=get_new_book_detail,
    )
    assert response.status_code == 409
    assert response.json() == BOOK_ALREADY_EXIST


def test_add_review(get_new_book_id):
    response = client.post(
        "/add-review/",
        json={
            "review": f"This is review for book {random.randint(10,500)}",
            "rating": random.randint(0,5),
            "bookID": get_new_book_id
            },
    )
    assert response.status_code == 200
    assert response.json() == REVIEW_ADDED_SUCCESSFULLY


def test_add_review_wrong_book_id(get_new_nonExcitant_book_id):
    response = client.post(
        "/add-review/",
        json={
            "review": f"This is review for book {random.randint(10,500)}",
            "rating": random.randint(0,5),
            "bookID": get_new_nonExcitant_book_id
            },
    )
    assert response.status_code == 409
    assert response.json() == BOOK_DOES_NOT_EXIST

def test_get_book_list_by_author(get_new_book_detail):
    response = client.post(
        "/get-book-list/",
        json={
            "Author": get_new_book_detail['author']
            },
    )
    assert response.status_code == 200

def test_get_book_list_by_publication_year(get_new_book_detail):
    response = client.post(
        "/get-book-list/",
        json={
            "publication_year": str(get_new_book_detail['publication_year'])
            },
    )
    assert response.status_code == 200

def test_get_all_book_list():
    response = client.post(
        "/get-book-list/",
        json={},
    )
    assert response.status_code == 200


def test_get_review_list(get_new_book_id):
    response = client.post(
        "/get-review-list/",
        json={
            "bookID": str(get_new_book_id)
            },
    )
    assert response.status_code == 200