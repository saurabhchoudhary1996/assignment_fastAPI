from pydantic import BaseModel, Field

#Add book entry
class BookEntry(BaseModel):
    title:str = Field(max_length=100)
    author:str = Field(max_length=100)
    publication_year:int

#Update book entry
class UpdateBookEntry(BaseModel):
    bookID: int
    title:str = Field(max_length=100)
    author:str = Field(max_length=100)
    publication_year:int

#delete book entry
class DeleteBookEntry(BaseModel):
    bookID: int

#add review entry
class ReviewEntry(BaseModel):
    review: str
    rating: int
    bookID: int

#update review entry
class UpdateReviewEntry(BaseModel):
    review: str
    rating: int
    reviewID: int
    
#delete review entry
class DeleteReviewEntry(BaseModel):
    reviewID: int
    

#fetch book list
class FetchBooks(BaseModel):
    author:str | None = None
    publication_year:str | None = None    

#Fetch review list
class FetchReviews(BaseModel):
    bookID: int