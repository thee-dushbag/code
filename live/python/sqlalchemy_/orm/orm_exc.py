import db_orm as db
import orm_model as tbl
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, MultipleResultsFound

ses = db.session

user = {"name": "Mark John", "age": 23, "email": "markjohn@gmail.com"}

if u := ses.query(tbl.User).filter_by(uid=1).first():
    u.name = "Simon Nganga"  # type: ignore
    u.age = 19  # type: ignore
    ses.add(u)
try:
    ses.commit()
except IntegrityError as e:
    print(f"Rolling back to safety")
    ses.rollback()
else:
    print("Update was successful")
finally:
    ses.close()
