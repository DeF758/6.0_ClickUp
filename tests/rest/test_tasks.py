import allure
import pytest
from datetime import datetime, timedelta
from scenarios.scenarios import create_task_and_get_body
from utils.helpers import Helper


@allure.feature("Валидация поля name при Создании и Изменении задачи")
class TestNameFieldCreateUpdateTask:
    valid_data = [
        pytest.param("T", id="Minimum value"),
        pytest.param("F" * 2048, id="Maximum value"),
        pytest.param("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", id="Latin alphabet"),
        pytest.param("1234567890", id="Numbers"),
        pytest.param("!@#$%^&*()_+{}[]':;?></.,-=`~", id="Special characters"),
        pytest.param("йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ", id="Cyrillic alphabet")
    ]

    @allure.story("Создание задачи с валидными данными в name")
    @pytest.mark.parametrize(
        "valid_name", valid_data)
    def test_name_field_create_task(self, auth_sess, get_gen_data, valid_name):
        payload = {"name": valid_name}
        invalid_task = auth_sess.create_task(payload)
        assert invalid_task.status_code == 200
        assert invalid_task.json()["name"] == valid_name

    @allure.story("Создание задачи с не валидными данными в name")
    @pytest.mark.parametrize(
        "invalid_name", [
            pytest.param(None, id="null"),
            pytest.param(1, id="Another type: int"),
            pytest.param(True, id="Another type: bool"),
            pytest.param("w" * 2049, id="Maximum allowed value")
        ], ids=str)
    def test_invalid_name_field_create_task(self, auth_sess, get_gen_data, invalid_name):
        payload = {"name": invalid_name}
        invalid_task = auth_sess.create_task(payload)
        assert invalid_task.status_code == 400

    @allure.story("Изменение задачи с валидными данными в name")
    @pytest.mark.parametrize(
        "valid_name", valid_data)
    def test_name_field_update_task(self, auth_sess, get_gen_data, valid_name):
        task_id, payload = create_task_and_get_body(auth_sess, "name", get_gen_data)
        payload["name"] = valid_name
        valid_task = auth_sess.update_task(task_id, payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["name"] == valid_name

    @allure.story("Изменение задачи с не валидными данными в name")
    @pytest.mark.parametrize(
        "invalid_name", [
            pytest.param(1, id="Another type: int"),
            pytest.param(True, id="Another type: bool"),
            pytest.param("w" * 2049, id="First invalid above")  # first invalid below
        ], ids=str)
    def test_invalid_name_field_update_task(self, auth_sess, get_gen_data, invalid_name):
        task_id, payload = create_task_and_get_body(auth_sess, "name", get_gen_data)
        payload["name"] = invalid_name
        invalid_task = auth_sess.update_task(task_id, payload)
        assert invalid_task.status_code == 400


@allure.feature("Валидация поля description при Создании и Изменении задачи")
class TestDescriptionFieldCreateUpdateTask:
    valid_data = [
        pytest.param("f", id="Minimum value"),
        pytest.param("F" * 262144, id="Maximum value"),
        pytest.param("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", id="Latin alphabet"),
        pytest.param("1234567890", id="Numbers"),
        pytest.param("!@#$%^&*()_+{}[]':;?></.,-=`~", id="Special characters"),
        pytest.param("йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ", id="Cyrillic alphabet")
    ]

    @allure.story("Создание задачи с валидными данными в description")
    @allure.title("Создание задачи с валидными данными в description: {valid_description}")
    @pytest.mark.parametrize(
        "valid_description", valid_data)
    def test_description_field_create_task(self, auth_sess, get_gen_data, valid_description):
        payload = {"name": get_gen_data.name, "description": valid_description}
        valid_task = auth_sess.create_task(payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["description"] == valid_description

    @allure.story("Создание задачи с игнорируемыми данными в description")
    @allure.title("Создание задачи с игнорируемыми данными в description: {unsaved_description}")
    @pytest.mark.parametrize(
        "unsaved_description", [
            pytest.param(None, id="null"),
            pytest.param(1, id="Another type: int"),
            pytest.param(True, id="Another type: bool"),
        ], ids=str)
    def test_unsaved_description_field_create_task(self, auth_sess, get_gen_data, unsaved_description):
        payload = {"name": get_gen_data.name, "description": unsaved_description}
        unsaved_description_task = auth_sess.create_task(payload)
        assert unsaved_description_task.status_code == 200
        assert unsaved_description_task.json()["description"] == ""

    @allure.story("Создание задачи с не валидными данными в description")
    @allure.title("Создание задачи с не валидными данными в description: {invalid_description}")
    @pytest.mark.parametrize(
        "invalid_description", [
            pytest.param("w" * 262145, id="First invalid above")
        ], ids=str)
    def test_invalid_description_field_create_task(self, auth_sess, get_gen_data, invalid_description):
        payload = {"name": get_gen_data.name, "description": invalid_description}
        invalid_task = auth_sess.create_task(payload)
        assert invalid_task.status_code == 413
        assert invalid_task.json()["err"] == "Task description is too long"

    @allure.story("Изменение задачи с валидными данными в description")
    @allure.title("Изменение задачи с валидными данными в description: {valid_description}")
    @pytest.mark.parametrize(
        "valid_description", valid_data, ids=str)
    def test_description_field_update_task(self, auth_sess, get_gen_data, valid_description):
        task_id, payload = create_task_and_get_body(auth_sess, "description", get_gen_data)
        payload["description"] = valid_description
        valid_task = auth_sess.update_task(task_id, payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["description"] == valid_description

    @allure.story("Изменение задачи с игнорируемыми данными в description")
    @allure.title("Изменение задачи с игнорируемыми данными в description: {unsaved_description}")
    @pytest.mark.parametrize(
        "unsaved_description", [
            pytest.param(1, id="Another type: int"),
            pytest.param(True, id="Another type: bool"),
            pytest.param([False], id="Another type: [bool]"),
            pytest.param([1], id="Another type: [int]"),
            pytest.param(["str"], id="Another type: [str]"),
        ], ids=str)
    def test_unsaved_description_field_update_task(self, auth_sess, get_gen_data, unsaved_description):
        task_id, payload = create_task_and_get_body(auth_sess, "description", get_gen_data)
        payload["description"] = unsaved_description
        unsaved_description_task = auth_sess.update_task(task_id, payload)
        assert unsaved_description_task.status_code == 200
        assert unsaved_description_task.json()["description"] == ""

    @allure.story("Изменение задачи с не валидными данными в description")
    @allure.title("Изменение задачи с не валидными данными в description: {invalid_description}")
    @pytest.mark.parametrize(
        "invalid_description", [
            pytest.param("w" * 262145, id="First invalid above")
        ], ids=str)
    def test_invalid_description_field_update_task(self, auth_sess, get_gen_data, invalid_description):
        task_id, payload = create_task_and_get_body(auth_sess, "description", get_gen_data)
        payload["description"] = invalid_description
        invalid_task = auth_sess.update_task(task_id, payload)
        assert invalid_task.status_code == 413
        assert invalid_task.json()["err"] == "Task description is too long"


@allure.feature("Валидация поля assignees при Создании и Изменении задачи")
class TestAssigneesFieldCreateUpdateTask:
    @allure.story("Создание задачи с игнорируемыми данными в assignees")
    @allure.title("Создание задачи с игнорируемыми данными в assignees: {unsaved_assignees}")
    @pytest.mark.parametrize(
        "unsaved_assignees", [
            pytest.param([2147483647], id="Maximum value"),
            pytest.param([0], id="Minimum value"),
            pytest.param(None, id="null"),
            pytest.param(1, id="Another type: [int]"),
            pytest.param(True, id="Another type: bool"),
            pytest.param(["str"], id="Another type: [str]"),
            pytest.param("xx", id="Another type: str"),
            pytest.param([True], id="Another type: [bool]")
        ], ids=str)
    def test_unsaved_assignees_field_create_task(self, auth_sess, get_gen_data, unsaved_assignees):
        payload = {"name": get_gen_data.name, "assignees": unsaved_assignees}
        valid_task = auth_sess.create_task(payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["assignees"] == []

    @allure.story("Создание задачи с не валидными данными в assignees")
    @allure.title("Создание задачи с не валидными данными в assignees: {invalid_assignees}")
    @pytest.mark.parametrize(
        "invalid_assignees", [
            pytest.param([2147483648], id="First invalid above")
        ], ids=str)
    def test_invalid_description_field_create_task(self, auth_sess, get_gen_data, invalid_assignees):
        payload = {"name": get_gen_data.name, "assignees": invalid_assignees}
        invalid_task = auth_sess.create_task(payload)
        assert invalid_task.status_code == 400
        assert invalid_task.json()["err"] == "Invalid assignee ID. Must be a valid integer."

    @allure.story("Изменение задачи с игнорируемыми данными в assignees")
    @allure.title("Изменение задачи с игнорируемыми данными в assignees: {unsaved_assignees}")
    @pytest.mark.parametrize(
        "unsaved_assignees", [
            pytest.param(None, id="null"),
            pytest.param(False, id="False"),
        ], ids=str)
    def test_unsaved_assignees_field_update_task(self, auth_sess, get_gen_data, unsaved_assignees):
        task_id, payload = create_task_and_get_body(auth_sess, "assignees", get_gen_data)
        payload["assignees"] = {"add": unsaved_assignees}
        unsaved_assignees_task = auth_sess.update_task(task_id, payload)
        assert unsaved_assignees_task.status_code == 200
        assert unsaved_assignees_task.json()["assignees"] == []

    @allure.story("Изменение задачи с не валидными данными в assignees")
    @allure.title("Изменение задачи с не валидными данными в assignees: {invalid_value}")
    @pytest.mark.parametrize(
        "invalid_value,ex_err,ex_code", [
            [[2147483647], "All assignees must have access to this task", 400],
            [["str"], "Assignees list invalid", 400],
            [[2147483648], "Internal Server Error", 500],
            ["xx", "Internal Server Error", 500],
            [[True], "Internal Server Error", 500]])
    def test_invalid_assignees_field_update_task(self, auth_sess, get_gen_data, invalid_value, ex_err, ex_code):
        task_id, payload = create_task_and_get_body(auth_sess, "assignees", get_gen_data)
        payload["assignees"] = {"add": invalid_value}
        invalid_task = auth_sess.update_task(task_id, payload)
        assert invalid_task.status_code == ex_code
        assert invalid_task.json()["err"] == ex_err


@allure.feature("Валидация поля archived при Создании и Изменении задачи")
class TestArchivedFieldCreateUpdateTask:
    valid_data = [True, False]
    unsaved_data = [
        pytest.param(2147483648, id="Another type: int "),
        pytest.param([0], id="Another type: [int] "),
        pytest.param("str", id="Another type: str "),
        pytest.param(["str"], id="Another type: [str] "),
        pytest.param([True], id="Another type: [bool] ")
    ]

    @allure.story("Создание задачи с валидными данными в archived")
    @allure.title("Создание задачи с валидными данными в archived: {valid_archived}")
    @pytest.mark.parametrize(
        "valid_archived", valid_data)
    def test_archived_field_create_task(self, auth_sess, get_gen_data, valid_archived):
        payload = {"name": get_gen_data.name, "archived": valid_archived}
        valid_task = auth_sess.create_task(payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["archived"] == valid_archived

    @allure.story("Создание задачи с игнорируемыми данными в archived")
    @allure.title("Создание задачи с игнорируемыми данными в archived: {unsaved_archived}")
    @pytest.mark.parametrize(
        "unsaved_archived", unsaved_data)
    def test_unsaved_archived_field_create_task(self, auth_sess, get_gen_data, unsaved_archived):
        payload = {"name": get_gen_data.name, "archived": unsaved_archived}
        unsaved_archived_task = auth_sess.create_task(payload)
        assert unsaved_archived_task.status_code == 200
        assert unsaved_archived_task.json()["archived"] == False

    @allure.story("Изменение задачи с валидными данными в archived")
    @allure.title("Изменение задачи с валидными данными в archived: {valid_archived}")
    @pytest.mark.parametrize(
        "valid_archived", valid_data, ids=str)
    def test_archived_field_update_task(self, auth_sess, get_gen_data, valid_archived):
        task_id, payload = create_task_and_get_body(auth_sess, "archived", get_gen_data)
        payload["archived"] = valid_archived
        valid_task = auth_sess.update_task(task_id, payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["archived"] == valid_archived

    @allure.story("Изменение задачи с не валидными данными в archived")
    @allure.title("Изменение задачи с не валидными данными в archived: {invalid_archived}")
    @pytest.mark.parametrize(
        "invalid_archived", unsaved_data)
    def test_unsaved_archived_field_update_task(self, auth_sess, get_gen_data, invalid_archived):
        task_id, payload = create_task_and_get_body(auth_sess, "archived", get_gen_data)
        payload["archived"] = invalid_archived
        invalid_task = auth_sess.update_task(task_id, payload)
        assert invalid_task.status_code == 500
        assert invalid_task.json()["err"] == "Internal Server Error"


@allure.feature("Валидация поля tags при Создании задачи")
class TestTagsFieldCreateTask:

    @allure.story("Создание задачи с валидными данными в tags")
    @allure.title("Создание задачи с валидными данными в tags: {valid_tags}")
    @pytest.mark.parametrize(
        "valid_tags", [
            pytest.param(["T"], id="Minimum value"),
            pytest.param(["F" * 100], id="Maximum value"),
            pytest.param(["qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"], id="Latin alphabet"),
            pytest.param(["1234567890"], id="Numbers"),
            pytest.param(["!@#$%^&*()_+{}[]':;?></.,-=`~"], id="Special characters"),
            pytest.param(["йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"], id="Cyrillic alphabet")
        ], ids=str)
    def test_tags_field_create_task(self, auth_sess, get_gen_data, valid_tags):
        payload = {"name": get_gen_data.name, "tags": valid_tags}
        valid_task = auth_sess.create_task(payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["tags"][0]["name"] == valid_tags[0].lower()

    @allure.story("Создание задачи с игнорируемыми данными в tags")
    @allure.title("Создание задачи с игнорируемыми данными в tags: {unsaved_tags}")
    @pytest.mark.parametrize(
        "unsaved_tags", [
            pytest.param("str", id="Another type: str "),
            pytest.param(1, id="Another type: int "),
            pytest.param(True, id="Another type: bool "),
        ], ids=str)
    def test_unsaved_tags_field_create_task(self, auth_sess, get_gen_data, unsaved_tags):
        payload = {"name": get_gen_data.name, "tags": unsaved_tags}
        unsaved_tags_task = auth_sess.create_task(payload)
        assert unsaved_tags_task.status_code == 200
        assert unsaved_tags_task.json()["tags"] == []

    @allure.story("Создание задачи с не валидными данными в tags")
    @allure.title("Создание задачи с не валидными данными в tags: {invalid_tags}")
    @pytest.mark.parametrize(
        "invalid_tags,err_msg", [
            pytest.param(["F" * 101], "Tag(s) are not valid", id="First invalid above"),
            pytest.param([0], "Invalid tag format", id="Another type: [int] "),
            pytest.param([True], "Invalid tag format", id="Another type: [bool] ")
        ], ids=str)
    def test_invalid_tags_field_create_task(self, auth_sess, get_gen_data, invalid_tags, err_msg):
        payload = {"name": get_gen_data.name, "tags": invalid_tags}
        invalid_task = auth_sess.create_task(payload)
        assert invalid_task.status_code == 400
        assert invalid_task.json()["err"] == err_msg


@allure.feature("Валидация поля status при Создании и Изменении задачи")
class TestStatusFieldCreateUpdateTask:
    valid_data = ["TO DO", "In Progress", "Ready to start Testing", "Testing", "Ready to Deploy", "Done", "Blocked"]

    @allure.story("Создание задачи с валидными данными в status")
    @allure.title("Создание задачи с валидными данными в status: {valid_value}")
    @pytest.mark.parametrize(
        "valid_value", valid_data)
    def test_status_field_create_task(self, auth_sess, get_gen_data, valid_value):
        payload = {"name": get_gen_data.name, "status": valid_value}
        valid_task = auth_sess.create_task(payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["status"]["status"] == valid_value.lower()

    @allure.story("Создание задачи с не валидными данными в status")
    @pytest.mark.parametrize(
        "invalid_value,ex_err,ex_code", [
            pytest.param(["str"], "Status must be a string", 400, id="Another type: [str] "),
            pytest.param(2147483647, "Status must be a string", 400, id="Another type: int "),
            pytest.param(True, "Status must be a string", 400, id="Another type: bool "),
            pytest.param("str", "Status not found", 400, id="Unregistered status "),
            pytest.param("T" * 4194251, "request entity too large", 413, id="First invalid above"),
            pytest.param([0], "Status must be a string", 400, id="Another type: [int] "),
            pytest.param([False], "Status must be a string", 400, id="Another type: [bool]")
        ], ids=str)
    def test_invalid_status_field_create_task(self, auth_sess, get_gen_data, invalid_value, ex_err, ex_code):
        payload = {"name": get_gen_data.name, "status": invalid_value}
        invalid_task = auth_sess.create_task(payload)
        assert invalid_task.status_code == ex_code
        assert invalid_task.json()["err"] == ex_err

    @allure.story("Изменение задачи с валидными данными в status")
    @allure.title("Изменение задачи с валидными данными в status: {valid_value}")
    @pytest.mark.parametrize(
        "valid_value", valid_data, ids=str)
    def test_status_field_update_task(self, auth_sess, get_gen_data, valid_value):
        task_id, payload = create_task_and_get_body(auth_sess, "status", get_gen_data)
        payload["status"] = valid_value
        valid_task = auth_sess.update_task(task_id, payload)
        assert valid_task.status_code == 200
        assert valid_task.json()["status"]["status"] == valid_value.lower()

    @allure.story("Изменение задачи с не валидными данными в status")
    @pytest.mark.parametrize(
        "invalid_value,ex_err,ex_code", [
            pytest.param(["str"], "Task status invalid", 400, id="Another type: [str] "),
            pytest.param(2147483647, "Task status invalid", 400, id="Another type: int "),
            pytest.param(True, "Task status invalid", 400, id="Another type: bool "),
            pytest.param("str", "Status does not exist", 400, id="Unregistered status "),
            pytest.param("T" * 4194250, "request entity too large", 413, id="First invalid above "),
            pytest.param([0], "Task status invalid", 400, id="Another type: [int] "),
            pytest.param([False], "Task status invalid", 400, id="Another type: [bool]")
        ])
    def test_invalid_status_field_update_task(self, auth_sess, get_gen_data, invalid_value, ex_err, ex_code):
        task_id, payload = create_task_and_get_body(auth_sess, "status", get_gen_data)
        payload["status"] = invalid_value
        invalid_task = auth_sess.update_task(task_id, payload)
        assert invalid_task.status_code == ex_code
        assert invalid_task.json()["err"] == ex_err


@allure.feature("Валидация полей start_date и due_date при Создании и Изменении задачи")
class TestDateFieldsCreateUpdateTask:
    yesterday = Helper.unix_conv(str((datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y %H:%M:%S")))
    tomorrow = Helper.unix_conv(str((datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y %H:%M:%S")))

    @allure.story("Создание задачи с валидными данными в start_date и due_date")
    @allure.title("Создание задачи с валидными данными в start_date и due_date: {start_valid}, {due_valid}")
    @pytest.mark.parametrize(
        "start_valid,due_valid", [
            pytest.param(Helper.unix_conv("01/01/1970"), Helper.unix_conv("31/12/1969 21:00:00"), id="Minimum value "),
            pytest.param(8639999989199999, 8639999989199999, id="Maximum value "),
            pytest.param(tomorrow, yesterday, id="start_date after due_date"),
        ])
    def test_start_due_date_field_create_task(self, auth_sess, get_gen_data, start_valid, due_valid):
        payload = {"name": get_gen_data.name, "start_date": start_valid, "due_date": due_valid}
        valid_task = auth_sess.create_task(payload)
        assert valid_task.status_code == 200

    @allure.story("Создание задачи с не валидными данными в start_date")
    @allure.title("Создание задачи с не валидными данными в start_date: {invalid_value}")
    @pytest.mark.parametrize(
        "invalid_value,ex_err,ex_code", [
            pytest.param(8639999989200000, "Internal Server Error", 500, id="First invalid above "),
            pytest.param("str", "Date invalid", 400, id="Unregistered status "),
            pytest.param([False], "Date invalid", 400, id="Another type: [bool]")
        ], ids=str)
    def test_invalid_start_date_field_create_task(self, auth_sess, get_gen_data, invalid_value, ex_err, ex_code):
        payload = {"name": get_gen_data.name, "start_date": invalid_value}
        invalid_task = auth_sess.create_task(payload)
        assert invalid_task.status_code == ex_code
        assert invalid_task.json()["err"] == ex_err

    @allure.story("Создание задачи с не валидными данными в due_date")
    @allure.title("Создание задачи с не валидными данными в due_date: {invalid_value}")
    @pytest.mark.parametrize(
        "invalid_value,ex_err,ex_code", [
            pytest.param(Helper.unix_conv("31/12/1969 20:59:59"), "Due date not valid, must be positive", 400,
                id="first invalid below "),
            pytest.param(8639999989200000, "Internal Server Error", 500, id="First invalid above "),
            pytest.param("str", "Date invalid", 400, id="Unregistered status "),
            pytest.param([False], "Date invalid", 400, id="Another type: [bool]")
        ], ids=str)
    def test_invalid_due_date_field_create_task(self, auth_sess, get_gen_data, invalid_value, ex_err, ex_code):
        payload = {"name": get_gen_data.name, "due_date": invalid_value}
        invalid_task = auth_sess.create_task(payload)
        assert invalid_task.status_code == ex_code
        assert invalid_task.json()["err"] == ex_err

    @allure.story("Изменение задачи с валидными данными в start_date и due_date")
    @allure.title("Изменение задачи с валидными данными в start_date и due_date: {start_valid}, {due_valid}")
    @pytest.mark.parametrize(
        "start_valid,due_valid", [
            pytest.param(Helper.unix_conv("01/01/0001"), Helper.unix_conv("01/01/0001"), id="Minimum value "),
            pytest.param(8639999899999999, 8639999899999999, id="Maximum value "),
            pytest.param(tomorrow, yesterday, id="start_date after due_date"),
        ], ids=str)
    def test_start_due_date_field_update_task(self, auth_sess, get_gen_data, start_valid, due_valid):
        task_id, payload = create_task_and_get_body(auth_sess, "start_date,due_date", get_gen_data)
        payload["start_date"] = start_valid
        payload["due_date"] = due_valid
        valid_task = auth_sess.update_task(task_id, payload)
        assert valid_task.status_code == 200

    @allure.story("Изменение задачи с не валидными данными в start_date")
    @allure.title("Изменение задачи с не валидными данными в start_date: {invalid_value}")
    @pytest.mark.parametrize(
        "invalid_value,ex_err,ex_code", [
            pytest.param(8639999989200000, "Internal Server Error", 500, id="First invalid above "),
            pytest.param("str", "Internal Server Error", 500, id="Unregistered status "),
            pytest.param([False], "Internal Server Error", 500, id="Another type: [bool]")
        ])
    def test_invalid_start_date_field_update_task(self, auth_sess, get_gen_data, invalid_value, ex_err, ex_code):
        task_id, payload = create_task_and_get_body(auth_sess, "start_date", get_gen_data)
        payload["start_date"] = invalid_value
        invalid_task = auth_sess.update_task(task_id, payload)
        assert invalid_task.status_code == ex_code
        assert invalid_task.json()["err"] == ex_err

    @allure.story("Изменение задачи с не валидными данными в due_date")
    @allure.title("Изменение задачи с не валидными данными в due_date: {invalid_value}")
    @pytest.mark.parametrize(
        "invalid_value,ex_err,ex_code", [
            pytest.param(8639999989200000, "Internal Server Error", 500, id="First invalid above "),
            pytest.param("str", "Date invalid", 400, id="Unregistered status "),
            pytest.param([False], "Date invalid", 400, id="Another type: [bool]")
        ])
    def test_invalid_due_date_field_update_task(self, auth_sess, get_gen_data, invalid_value, ex_err, ex_code):
        task_id, payload = create_task_and_get_body(auth_sess, "due_date", get_gen_data)
        payload["due_date"] = invalid_value
        invalid_task = auth_sess.update_task(task_id, payload)
        assert invalid_task.status_code == ex_code
        assert invalid_task.json()["err"] == ex_err


@allure.feature("Проверка Get, Update, Delete")
class TestGetUpdateDeleteTask:
    @allure.title("Проверка Get")
    def test_get_task(self, auth_sess, get_gen_data, get_task_id):
        with allure.step("Получение задачи по id"):
            get_task = auth_sess.get_task(get_task_id)
            assert get_task.status_code == 200
            assert get_task.json()["id"] == get_task_id

        with allure.step("Получение задачи по id с description в markdown"):
            get_markdown_task = auth_sess.get_task(get_task_id, include_markdown_description="true")
            assert get_markdown_task.status_code == 200
            assert get_markdown_task.json()["markdown_description"] == get_gen_data.description

        with allure.step("Удаление задачи"):
            assert auth_sess.delete_task(get_task_id).status_code == 204

        with allure.step("Получение удалённой задачи"):
            get_deleted_task = auth_sess.get_task(get_task_id)
            assert get_deleted_task.status_code == 404
            assert get_deleted_task.json()["err"] == "Task not found, deleted"

        with allure.step("Получение задачи по не валидному id"):
            get_int_task = auth_sess.get_task(123)
            assert get_int_task.status_code == 401
            assert get_int_task.json()["err"] == "Team not authorized"

        with allure.step("Получение задачи без id"):
            get_empty_task = auth_sess.get_task("")
            assert get_empty_task.status_code == 404
            assert get_empty_task.json()["err"] == "Route not found"

    @allure.title("Проверка Update")
    def test_update_task(self, auth_sess, get_gen_data, get_task_id):
        with allure.step("Обновление задачи по id"):
            assert auth_sess.update_task(get_task_id).status_code == 200

        with allure.step("Удаление задачи"):
            assert auth_sess.delete_task(get_task_id).status_code == 204

        with allure.step("Обновление удалённой задачи"):
            update_deleted_task = auth_sess.get_task(get_task_id)
            assert update_deleted_task.status_code == 404
            assert update_deleted_task.json()["err"] == "Task not found, deleted"

        with allure.step("Обновление задачи по не валидному id"):
            update_int_task = auth_sess.update_task(123)
            assert update_int_task.status_code == 401
            assert update_int_task.json()["err"] == "Team not authorized"

        with allure.step("Обновление задачи по пустому id"):
            assert auth_sess.update_task("").status_code == 404

    @allure.title("Проверка Delete")
    def test_delete_task(self, auth_sess, get_gen_data, get_task_id):
        with allure.step("Удаление задачи"):
            assert auth_sess.delete_task(get_task_id).status_code == 204

        with allure.step("Проверка, что задача удалена"):
            get_deleted_task = auth_sess.get_task(get_task_id)
            assert get_deleted_task.status_code == 404
            assert get_deleted_task.json()["err"] == "Task not found, deleted"

        with allure.step("Удаление удалённой задачи"):
            assert auth_sess.delete_task(get_task_id).status_code == 204

        with allure.step("Удаление задачи по не валидному id"):
            delete_int_task = auth_sess.delete_task(123)
            assert delete_int_task.status_code == 401
            assert delete_int_task.json()["err"] == "Team not authorized"

        with allure.step("Удаление задачи по пустому id"):
            delete_empty_task = auth_sess.delete_task("")
            assert delete_empty_task.status_code == 404
