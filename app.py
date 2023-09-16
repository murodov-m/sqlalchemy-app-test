from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy.orm import sessionmaker

from db.models import Project, Client, ProjectShots, engine, Application
from serializers import ApplicationRequest


app = FastAPI()
admin = Admin(app, engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

@app.post('/application/create/', response_model=ApplicationRequest)
async def application(app: ApplicationRequest):
    db = SessionLocal()
    db_app = Application(**app.dict())
    # TODO: send to telegram message
    # requests.post("https://api.telegram.org/bot{TOKEN_HERE}/sendMessage", data={"chat_id": -10012312312, "message": "Privet"})
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    db.close()
    print(app.dict())
    return app

from typing import Any
class ProjectAdmin(ModelView, model=Project):
    column_list = ["title", "description", "image"]
    form_excluded_columns = ["project_shots"]

    def get_list_value(self, obj: Any, prop: str):
        obj = super().get_list_value(obj, prop)
        
        if prop == "image":
            print(obj, "prop")
            return (
                f"<img src={obj[0]} alt={obj[0]} />", 
                f"<img src={obj[0]} alt={obj[0]} />")
        return obj

class ClientAdmin(ModelView, model=Client):
    column_list = ["email", "full_name", "phone_number"]

class ProjectShotsAdmin(ModelView, model=ProjectShots):
    column_list = ["project_id",]
    

class ApplicationAdmin(ModelView, model=Application):
    column_list = ["phone", "message"]

admin.add_view(ProjectAdmin)
admin.add_view(ClientAdmin)
admin.add_view(ProjectShotsAdmin)
admin.add_view(ApplicationAdmin)