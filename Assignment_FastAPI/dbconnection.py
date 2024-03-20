import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
load_dotenv()


class Initialize_Database:
    def __init__(self) -> None:
        self._conn = psycopg2.connect(
            host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), port=os.getenv('post'))
        self._conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self._cur = self._conn.cursor()

    def createDatabase(self):
        self._cur.execute("CREATE DATABASE %s;" % os.getenv('database'))

    def getDatabaseNameList(self):
        sql = 'SELECT datname FROM pg_database;'
        self._cur.execute(sql)
        info = self._cur.fetchall()
        return info

class DataBase:
    def __init__(self) -> None:
        self._conn = psycopg2.connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'),
                                      database=os.getenv('database'), port=os.getenv('post'))
        self._cur = self._conn.cursor(cursor_factory=RealDictCursor)

    def db_commit(self):
        self._conn.commit()

    def db_close(self):
        if self._cur is not None:
            self._cur.close()
        self._cur = None
        
        if self._conn is not None:
            self._conn.close()
        self._conn = None

    def db_rollback(self):
        self._conn.rollback()
    
    def createTables(self):
        sql = '''
                CREATE TABLE IF NOT EXISTS book(
					book_id SERIAL PRIMARY KEY,
					title VARCHAR(100) NOT NULL,
					author VARCHAR(100) NOT NULL,
					publication_year INT NOT NULL,
					UNIQUE(title)
				);

                CREATE TABLE IF NOT EXISTS book_review(
					review_id SERIAL PRIMARY KEY,
					book_id INT NOT NULL,
					review VARCHAR(500) NOT NULL,
					rating SMALLINT NOT NULL,
                    CONSTRAINT fk_book FOREIGN KEY(book_id) REFERENCES book(book_id) on delete cascade
				);
                
            '''
        self._cur.execute(sql)


    def db_add_book(self, title, author, publication_year):
        try:
            sql = 'INSERT INTO book(title, author, publication_year) VALUES(%s,%s,%s);'
            self._cur.execute(sql, [title, author, publication_year])
        except:
            raise

    def db_update_book(self, bookID, title, author, publication_year):
        try:
            sql = 'UPDATE book SET title = %s, author = %s, publication_year = %s WHERE book_id = %s;'
            self._cur.execute(sql, [title, author, publication_year, bookID])
        except:
            raise

    def db_delete_book(self, bookID):
        try:
            sql = 'DELETE FROM book WHERE book_id = %s;'
            self._cur.execute(sql, [bookID])
        except:
            raise

    def db_add_review(self, bookID, review, rating):
        try:
            sql = 'INSERT INTO book_review(book_id, review, rating) VALUES(%s,%s,%s);'
            self._cur.execute(sql, [bookID, review, rating])
        except:
            raise

    def db_update_review(self, reviewID, review, rating):
        try:
            sql = 'UPDATE book_review SET review = %s, rating = %s WHERE review_id = %s;'
            self._cur.execute(sql, [review, rating, reviewID])
        except:
            raise

    def db_delete_review(self, reviewID):
        try:
            sql = 'DELETE FROM book_review WHERE review_id = %s;'
            self._cur.execute(sql, [reviewID])
        except:
            raise

    def db_check_book_exist_title(self, title):
        try:
            sql = 'SELECT EXISTS(SELECT * from book WHERE title = %s);'
            self._cur.execute(sql, [title])
            info = self._cur.fetchone()
            return info
        except:
            raise
    
    def db_check_book_exist_bookID(self, bookID):
        try:
            sql = 'SELECT EXISTS(SELECT * from book WHERE book_id = %s);'
            self._cur.execute(sql, [bookID])
            info = self._cur.fetchone()
            return info
        except:
            raise

    def db_check_review_exist(self, reviewID):
        try:
            sql = 'SELECT EXISTS(SELECT * from book_review WHERE review_id = %s);'
            self._cur.execute(sql, [reviewID])
            info = self._cur.fetchone()
            return info
        except:
            raise

    def db_get_book_review(self, bookID):
        try:
            sql = '''SELECT review_id, review, rating FROM book_review WHERE book_id = %s;'''
            self._cur.execute(sql, [bookID])
            info = self._cur.fetchall()
            return info
        except:
            raise

    def db_get_book_list_by_author(self, author):
        try:
            sql = '''SELECT book_id, title, author, publication_year FROM book WHERE author = %s;'''
            self._cur.execute(sql, [author])
            info = self._cur.fetchall()
            return info
        except:
            raise

    def db_get_book_list_by_publication_year(self, publication_year):
        try:
            sql = '''SELECT book_id, title, author, publication_year FROM book WHERE publication_year = %s;'''
            self._cur.execute(sql, [publication_year])
            info = self._cur.fetchall()
            return info
        except:
            raise

    def db_get_all_book_list(self):
        try:
            sql = '''SELECT book_id, title, author, publication_year FROM book;'''
            self._cur.execute(sql)
            info = self._cur.fetchall()
            return info
        except:
            raise

    
    

    

        
    
     

    



def init():
    IB = Initialize_Database()
    try:
        if (os.getenv('database'),) not in IB.getDatabaseNameList():
            IB.createDatabase()
        db = DataBase()
        try:
            db.createTables()
            db.db_commit()
        except Exception as e:
            print('error occurred while creating tables')
            print(e)
            db.db_rollback()
            pass
        finally:
            db.db_close()
    except Exception as ce:
        print('Error occurred while creating database')
        print(ce)
        pass
    finally:
        IB._cur.close()
    

init()