from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from db.database import direct_get_conn, context_get_conn
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from schema.blog_schema import BlogData
from util.util import truncate_text
from sqlalchemy.engine import Connection


router = APIRouter(prefix="/blogs", tags=["blogs"])

# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_all_blogs(request: Request):

    conn = None
    try:
        conn = direct_get_conn()
        query = """
        SELECT id, title, author, content, image_loc, modified_dt FROM blog;
        """
        result = conn.execute(text(query))
        all_blogs = [BlogData(id=row.id,
              title=row.title,
              author=row.author,
              content=truncate_text(row.content),
              image_loc=row.image_loc, 
              modified_dt=row.modified_dt) for row in result]
        
        result.close()
        return templates.TemplateResponse(
            request = request,
            name = "index.html",
            context = {"all_blogs": all_blogs}
        )
    
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 서비스 오류가 발생하였습니다")
    finally:
        if conn:
            conn.close()


@router.get("/show/{id}")
def get_blog_by_id(request: Request,
                   id: int,
                   conn: Connection = Depends(context_get_conn)):
    
    try:
        query = """
        SELECT id, title, author, content, image_loc, modified_dt FROM blog
        WHERE id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)

        # 만약 한건도 찾미 못하면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"해당 {id} 블로그를 찾을 수 없습니다.")
        
        row = result.fetchone()
        blog = BlogData(id=row.id,
                        title=row.title,
                        author=row.author,
                        content=row.content,
                        image_loc=row.image_loc,
                        modified_dt=row.modified_dt)
        result.close()

        return templates.TemplateResponse(
            request = request,
            name = "show_blog.html",
            context = {"blog": blog}
        )
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="알수없는 이유로 서비스 오류가 발생하였습니다")
    

@router.get("/new")
def create_blog_ui(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "new_blog.html",
        context = {}
    )

@router.post("/new")
def create_blog(request: Request
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        INSERT INTO blog (title, author, content, modified_dt) VALUES ('{title}', '{author}', '{content}', now());
        """
        conn.execute(text(query))
        conn.commit() # 트랜잭션 커밋

        return RedirectResponse(url="/blogs", status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="요청데이터가 제대로 전달되지 않았습니다.")
    


@router.get("/modify/{id}")
def update_blog_ui(request: Request, id: int, conn = Depends(context_get_conn)):
    try:
        query = f"""
        select id, title, author, content from blog where id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        row = result.fetchone()
    
        return templates.TemplateResponse(
            request = request,
            name="modify_blog.html",
            context = {"id": row.id, "title": row.title,
                       "author": row.author, "content": row.content}
        )
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="요청데이터가 제대로 전달되지 않았습니다.")


@router.post("/modify/{id}")
def update_blog(request: Request, id: int
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn: Connection = Depends(context_get_conn)):
    
    try:
        query = f"""
        UPDATE blog 
        SET title = :title , author= :author, content= :content
        where id = :id
        """
        bind_stmt = text(query).bindparams(id=id, title=title, 
                                           author=author, content=content)
        result = conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않아 update 건수가 없으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        conn.commit()
        return RedirectResponse(f"/blogs/show/{id}", status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="요청데이터가 제대로 전달되지 않았습니다. ")
    

@router.post("/delete/{id}")
def delete_blog(request: Request, id: int
                , conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        DELETE FROM blog
        where id = :id
        """

        bind_stmt = text(query).bindparams(id=id)
        result = conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않아 delete 건수가 없으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        conn.commit()
        return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)

    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다.")