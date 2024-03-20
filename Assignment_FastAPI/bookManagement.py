from dbconnection import DataBase
from constantVariables import *
from datetime import datetime
import asyncio

class BookManagement:
    def __init__(self) -> None:
        pass

    def addBook(self, data):
        title = data.title
        author = data.author
        publication_year = data.publication_year
        
        db = DataBase()
        try:
            #Book entry should be unique to avoid duplication
            if db.db_check_book_exist_title(title=title)['exists'] == False:
                #Check whether publication date is valid or not
                if self.__isYearValid(publication_year=publication_year):
                    db.db_add_book(title, author, publication_year)
                    db.db_commit()
                    return BOOK_ADDED_SUCCESSFULLY
                else:
                    return INVALID_YEAR_VALUE
            else:
                return BOOK_ALREADY_EXIST
        except Exception as e:
            print(e)
            db.db_rollback()
            raise
        finally:
            db.db_close()

    def updateBook(self, data):
        bookID = data.bookID
        title = data.title
        author = data.author
        publication_year = data.publication_year
        
        db = DataBase()
        try:
            #Book entry should exist for updation
            if db.db_check_book_exist_bookID(bookID=bookID)['exists']:
                #Check whether publication date is valid or not
                if self.__isYearValid(publication_year=publication_year):
                    db.db_update_book(bookID, title, author, publication_year)
                    db.db_commit()
                    return BOOK_UPDATED_SUCCESSFULLY
                else:
                    return INVALID_YEAR_VALUE
            else:
                return BOOK_DOES_NOT_EXIST
        except Exception as e:
            print(e)
            db.db_rollback()
            raise
        finally:
            db.db_close()

    def deleteBook(self, data):
        bookID = data.bookID
        
        db = DataBase()
        try:
            db.db_delete_book(bookID)
            db.db_commit()
            return BOOK_DELETED_SUCCESSFULLY
        except Exception as e:
            print(e)
            db.db_rollback()
            raise
        finally:
            db.db_close()

    def addReview(self, data):
        bookID = data.bookID
        review = data.review
        rating = data.rating
        
        db = DataBase()
        try:
            #Check whether book is exist or not
            #if exist add review and return success message
            #else return not exist message
            if db.db_check_book_exist_bookID(bookID = bookID)['exists']:
                db.db_add_review(bookID, review, rating)
                db.db_commit()
                return REVIEW_ADDED_SUCCESSFULLY
            else:
                return BOOK_DOES_NOT_EXIST
        except Exception as e:
            print(e)
            db.db_rollback()
            raise
        finally:
            db.db_close()

    def updateReview(self, data):
        reviewID = data.reviewID
        review = data.review
        rating = data.rating
        
        db = DataBase()
        try:
            #Check whether review is exist or not
            #if exist update review and return success message
            #else return not exist message
            if db.db_check_review_exist(reviewID = reviewID)['exists']:
                db.db_update_review(reviewID, review, rating)
                db.db_commit()
                return REVIEW_UPDATED_SUCCESSFULLY
            else:
                return REVIEW_DOES_NOT_EXIST
        except Exception as e:
            print(e)
            db.db_rollback()
            raise
        finally:
            db.db_close()

    def deleteReview(self, data):
        reviewID = data.reviewID
        
        db = DataBase()
        try:
            #delete review
            db.db_delete_review(reviewID)
            db.db_commit()
            return REVIEW_DELETED_SUCCESSFULLY
            
        except Exception as e:
            print(e)
            db.db_rollback()
            raise
        finally:
            db.db_close()

    def fetchBooks(self, data):
        author = data.author 
        publication_year = data.publication_year    
        if self.__isFilterValid(author, publication_year):
            db = DataBase()
            try:
                #If author mentioned, fetch book data by author
                if author:
                    book_detail_list = db.db_get_book_list_by_author(author=author)
                #If publication year mentioned, fetch book data by publication year
                elif publication_year:
                    book_detail_list = db.db_get_book_list_by_publication_year(publication_year=publication_year)
                # Both are not mentioned, fetch all books
                else:
                    book_detail_list = db.db_get_all_book_list()

                return book_detail_list
            except Exception as e:
                print(e)
                raise
            finally:
                db.db_close()
        else:
            return INVALID_FILTER_TYPE

    def fetchReview(self, data):
        bookID = data.bookID
        db = DataBase()
        try:
            #Check book is exist or not
            #If exist return list of review, rating of that book
            #Else return not exist message
            if db.db_check_book_exist_bookID(bookID = bookID)['exists']:
                review_list = db.db_get_book_review(bookID=bookID)    
                return review_list
            else:
                return BOOK_DOES_NOT_EXIST
        except Exception as e:
            print(e)
            raise
        finally:
            db.db_close()

    #publication year must be valid and in between 1900, current year
    def __isYearValid(self, publication_year:int):
        return True if publication_year >=1900 and publication_year <=datetime.today().year else False
    
    #User can filter only either author or publication(By not mentioning both, user can fet all book list)
    #User cannot filter by mentioning author and publication
    def __isFilterValid(self, author, publication_year):
        #checking only one is mentioned or not
        return False if author and publication_year else True
    
    #Email will be send here 
    async def send_notification(self, review):
        await asyncio.sleep(2)
 

    
    
                
            

