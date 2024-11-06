import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from config import DB_JSON

app = FastAPI()

@app.get("/", operation_id="some_specific_id_you_define")
def get_json():
    with open(DB_JSON, 'r', encoding='utf-8') as file:
        data = json.load(file)

    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    return Response(
        content=json_data,
        media_type='application/json'
    )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
