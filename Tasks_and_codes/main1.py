from fastapi import FastAPI, Path, HTTPException, Query, UploadFile #type:ignore
from fastapi.responses import JSONResponse #type: ignore
from fastapi.middleware.cors import CORSMiddleware  #type: ignore
from pydantic import BaseModel, Field  #type: ignore
from typing import Annotated, Optional
import json

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#for post - new contact addition
class contact_list(BaseModel):
    id: Annotated[str, Field(..., description = "ID for storing the contact details", examples=['C001'])]
    name:Annotated[str, Field(..., description = "Name of the person ")]
    contact_number: Annotated[str, Field(..., description = "Mobile Number of the person", min_length=10, max_length=10)]

class edit_model(BaseModel): # type: ignore
    name: Annotated[Optional[str], Field(default= None)]
    contact_number: Annotated[Optional[str], Field(default=None)]

def load_data():
    with open('contact_list.json', 'r') as f:
        df = json.load(f)
    return df

def save_data(df):
    with open('contact_list.json', 'w') as f:
        json.dump(df, f)


@app.get('/')
def about():
    return {'message': 'This is the Day 2 Task 1'}

@app.get('/view')
def view():
    df = load_data()
    return df

#GET for FastAPI
@app.get('/view/{contact_id}')
def search(contact_id: str=Path(... , description= 'Contact ID of the person', example="C001")):
    df = load_data()
    if contact_id in df:
        return df[contact_id]
    else:
        return{'error': 'contact details for {contact_id} not available'}

#POST for FastAPI
@app.post('/create')
def create_contact(contact: contact_list):
    df = load_data()

    if contact.id in df:
        raise HTTPException(status_code=400, detail = 'Contact Already Exists')
    
    df[contact.id] = contact.model_dump(exclude= ['id'])
    save_data(df)
    return JSONResponse(status_code= 200, content={'message':'Contact details added!'})

#Put for FastAPI #Include contact id and request body
@app.put('/edit/{contact_id}')
def update(contact_id: str, contact_edit: edit_model):
    df = load_data()

    if contact_id not in df:
        raise HTTPException(status_code= 400, detail="Patient not found in the available in the data.")

    existing_contact = df[contact_id]

    updated_contact_details = contact_edit.model_dump(exclude_unset=True) # unset because update only the values given by client. If not 'exclude_unset = True', requires all.
    
    for key, value in updated_contact_details.items():
        existing_contact[key] = value

    df[contact_id] = existing_contact

    save_data(df)
    return JSONResponse(status_code= 200, content={'message':'Contact details updated}!'})


# Delete for FastAPI 
@app.delete('/delete/{contact_id}')
def delete_contact(contact_id: str):

    df = load_data()

    if contact_id not in df:
        raise HTTPException(status_code=400, detail= 'There is no contact with that id.')
    
    del df[contact_id]
    
    save_data(df)
    
    return JSONResponse(status_code= 200, content={'message':'The contact has been permanantly deleted!'})


@app.post("/upload")
async def upload_image(upload_file: UploadFile):
    content = await upload_file.read()
    size_kb = round(len(content) / 1024, 2)
    metadata = {
        "filename": upload_file.filename,
        "size_kb": size_kb,
        "mime_type": upload_file.content_type,
    }

    return JSONResponse(content=metadata)
                