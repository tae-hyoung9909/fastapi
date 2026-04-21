1. DB 생성 (MySQL)
 - initial_data.sql 이용하여 DB 생성

2. DB 연결 (database.py)
 - pip install mysql-connector-python
 - create_engine 생성 -> conn = connect() 연결
 - 생성된 conn을 불러옴 -> conn.execute() 쿼리 실행 -> close() 종료하고 반납

3. schema 생성
 - pydantic 

4. 데이터 읽어오기
 - jinja2 template 엔진
 - templates/index.html
 - 이때 content 본문이 너무 길기 때문에 utli.py에서 조정

5. 개별 id별로 조회
 - :id , bindparms(id=id) 이용

6. 글 생성하기
 - 글 생성할 UI 만들어준다.
 - POST API 만들어준다.
 - INSERT 후 COMMIT

7. 글 수정하기
 
8. 글 삭제하기