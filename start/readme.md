# FastAPI

#### FastAPI 실행 방법
```
uvicorn main:app --reload --port 8080
```
* http://localhost:8080로 접근

#### Swagger UI
* Swagger UI는 API들을 브라우저 기반에서 편리하게 관리 및 문서화, 테스트 할 수 있는 기능을 제공

##### 사용법
* `/docs`로 접근
* summary, tags, description로 문서화 가능
* description은 ''' '''으로 마크다운으로 작성 가능

```python
async def root():
    '''
    이쪽 부분에 마크다운 작성
    '''
    return {"message": "Hello World"} # application/json으로 반환

```

