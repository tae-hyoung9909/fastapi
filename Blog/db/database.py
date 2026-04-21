from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status
from fastapi.exceptions import HTTPException




DATABASE_CONN = "mysql+mysqlconnector://root:1234@localhost:3306/blog_db"


engine = create_engine(DATABASE_CONN, #echo=True,
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10, max_overflow=0,
                       pool_recycle=300)

def direct_get_conn():
    conn = None
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                            detail="요처아신 서비스가 잠시 내부적으로 문제가 발생했습니다")
    

# generator + fastapi dependency injection
def context_get_conn():
    conn = None
    try:
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요처아신 서비스가 잠시 내부적으로 문제가 발생했습니다")
    finally:
        if conn:
            conn.close()
