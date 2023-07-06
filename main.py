from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db',check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            );
            """)

app = FastAPI()

@app.post('/items')
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]):

    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items(title,image,price,description,place,insertAt)
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt})
                """)
    # hex-16진법으로 
    con.commit()
    return '200'

@app.get('/items')
async def get_items():
    # 컬럼명도 같이 가져옴
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    # connection의 현재 위치를 cursor라고 표시 위치 업데이트
    rows = cur.execute(f"""
                       SELECT * from items;
                       """).fetchall() 
                            # cur.execute().fetchall() 가져오는 문법
    return JSONResponse(jsonable_encoder(
        dict(row) for row in rows
        ))
    # rows줄 중에 각각의 array를 돌면서 array를 dictionary, 객체 형태로 만들어주는 문법
    # rows = [['id':1],['title':'애옹'],['description':'애오옹']...]
    # => {id:1,title:'애옹',description:'애오옹'}

@app.get('/images/{item_id}')
async def get_image(item_id):
    cur=con.cursor()
    # 16진법
    image_bytes=cur.execute(f"""
                            SELECT image from items WHERE id={item_id}
                            """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes),media_type='image/*') 
    # 저장할 때는 16진법으로 저장하고 다시 2진법으로 바꿔서 보여주는
    

app.mount("/", StaticFiles(directory="frontend",html=True),name="frontend")