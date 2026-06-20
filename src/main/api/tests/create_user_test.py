import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User



@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session:Session):
        response = api_manager.admin_steps.create_user(create_user_request)


        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Пользователь создан, но его нет в бд"



    @pytest.mark.parametrize(
        "username, password",
        [
            ("бра", "Pas!sw0rd"),
            ("Vl", "Pas!sw0rd"),
            ("vls!", "Pas!sw0rd"),
            ("Vlesss1", "Pas!sw0rд"),
            ("Vlesss2", "Pas!sw0"),
            ("Vlesss3", "pas!sw0rd"),
            ("Vlesss4", "PAS!SWORD"),
            ("Vlesss5", "PASSSWORD"),
            ("Vlesss6", "PAS!SWRD")
        ]
    )
    def test_create_user_invalid(self,db_session:Session ,username:str, password:str, api_manager:ApiManager):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, "Пользователь создан, ошибка"



