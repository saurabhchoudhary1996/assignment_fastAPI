# from fastapi import FastAPI
from fastapi import FastAPI,Response, status, BackgroundTasks
from bookManagement import BookManagement
from constantVariables import *
from fastapi.encoders import jsonable_encoder
from BaseModels import *


app = FastAPI()




@app.post("/add-book/")
async def addBook(data:BookEntry, response: Response):
    try:
        bookManagementObj = BookManagement()
        result = bookManagementObj.addBook(data)

        if result == BOOK_ADDED_SUCCESSFULLY:
            response.status_code = status.HTTP_200_OK
        elif result == BOOK_ALREADY_EXIST:
            response.status_code = status.HTTP_409_CONFLICT
        elif result == INVALID_YEAR_VALUE:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        print(e)
        result = UNABLE_TO_ADD_BOOK
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonable_encoder(result)

@app.post("/update-book/")
async def updateBook(data:UpdateBookEntry, response: Response):
    try:
        bookManagementObj = BookManagement()
        result = bookManagementObj.updateBook(data)

        if result == BOOK_UPDATED_SUCCESSFULLY:
            response.status_code = status.HTTP_200_OK
        elif result == BOOK_DOES_NOT_EXIST:
            response.status_code = status.HTTP_409_CONFLICT
        elif result == INVALID_YEAR_VALUE:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        print(e)
        result = UNABLE_TO_UPDATE_BOOK
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonable_encoder(result)

@app.post("/delete-book/")
async def deleteBook(data:DeleteBookEntry, response: Response):
    try:
        bookManagementObj = BookManagement()
        result = bookManagementObj.deleteBook(data)

        if result == BOOK_DELETED_SUCCESSFULLY:
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        print(e)
        result = UNABLE_TO_DELETE_BOOK
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonable_encoder(result)

@app.post("/add-review/")
async def addReview(data: ReviewEntry, response: Response, background_task: BackgroundTasks):
    try:
        result= data
        bookManagementObj = BookManagement()
        result = bookManagementObj.addReview(data)

        if result == REVIEW_ADDED_SUCCESSFULLY:
            background_task.add_task(bookManagementObj.send_notification, data)
            response.status_code = status.HTTP_200_OK
        elif result == BOOK_DOES_NOT_EXIST:
            response.status_code = status.HTTP_409_CONFLICT
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        print(e)
        result = UNABLE_TO_ADD_REVIEW
        # response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonable_encoder(result)

@app.post("/update-review/")
async def updateReview(data: UpdateReviewEntry, response: Response, background_task: BackgroundTasks):
    try:
        bookManagementObj = BookManagement()
        result = bookManagementObj.updateReview(data)

        if result == REVIEW_UPDATED_SUCCESSFULLY:
            background_task.add_task(bookManagementObj.send_notification, data)
            response.status_code = status.HTTP_200_OK
        elif result == REVIEW_DOES_NOT_EXIST:
            response.status_code = status.HTTP_409_CONFLICT
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        print(e)
        result = UNABLE_TO_UPDATE_REVIEW
        # response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonable_encoder(result)

@app.post("/delete-review/")
async def deleteReview(data: DeleteReviewEntry, response: Response):
    try:
        result= data
        bookManagementObj = BookManagement()
        result = bookManagementObj.deleteReview(data)

        if result == REVIEW_DELETED_SUCCESSFULLY:
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        print(e)
        result = UNABLE_TO_DELETE_REVIEW
        # response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonable_encoder(result)

@app.post("/get-book-list/")
async def getBookList(data:FetchBooks, response: Response = 200):
    try:
        bookManagementObj = BookManagement()
        result = bookManagementObj.fetchBooks(data)

        if result == INVALID_FILTER_TYPE:
            response.status_code = status.HTTP_409_CONFLICT
        else:
            response.status_code = status.HTTP_200_OK

    except Exception as e:
        print(e)
        result = UNABLE_TO_FETCH_BOOK_LIST
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonable_encoder(result)

@app.post("/get-review-list/")
async def getReviewList(data: FetchReviews, response: Response):
    try:
        bookManagementObj = BookManagement()
        result = bookManagementObj.fetchReview(data)

        if result == BOOK_DOES_NOT_EXIST:
            response.status_code = status.HTTP_409_CONFLICT
        else:
            response.status_code = status.HTTP_200_OK

    except Exception as e:
        print(e)
        result = UNABLE_TO_FETCH_BOOK_LIST
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonable_encoder(result)

