import allure
from random import randint, choice, sample

from scenarios.scenarios import csdc, check_cr_invalid_map
from utils.helpers import Helper


class TestTask:
    def test_create_task(self, auth_sess, get_gen_data, get_gen_req_field):
        task_data = get_gen_data
        # task_data.archived = False
        first_task = auth_sess.create_task(data=task_data)
        assert first_task.status_code == 200
        assert auth_sess.get_task(first_task.json()["id"]).status_code == 200

        with allure.step("Создание задачи с названием больше допустимого"):
            sec_data = task_data.copy()
            sec_data.name = "w" * 2049
            sec_task = auth_sess.create_task(data=sec_data)
            assert sec_task.status_code == 400

        task_data = get_gen_data
        sec_task = auth_sess.create_task(data=task_data)
        assert sec_task.status_code == 200

        assert auth_sess.create_task(data=get_gen_req_field).status_code == 200

    def test_required_field_create_update_task(self, auth_sess, get_gen_data, get_gen_req_field):
        required_field = {"name": get_gen_data.name}

        valid_data = ["!@#$%^&*()_+{}[]':;?></.,-=`~",
            "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ", "1234567890",
            "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", "F" * 2048]
        invalid_data = [None, 1, True, "w" * 2049]

        with allure.step("Создание задачи с валидными данными в name"):
            for valid_name in valid_data:
                required_field["name"] = valid_name
                valid_task = auth_sess.create_task(required_field)
                assert valid_task.status_code == 200

        with allure.step("Создание задачи с не валидными данными в name"):
            for invalid_name in invalid_data:
                required_field["name"] = invalid_name
                invalid_task = auth_sess.create_task(required_field)
                assert invalid_task.status_code == 400

        task_id = valid_task.json()["id"]

        with allure.step("Изменение задачи с валидными данными в name"):
            for valid_name in valid_data:
                required_field["name"] = valid_name
                valid_task = auth_sess.update_task(task_id, required_field)
                assert valid_task.status_code == 200

        with allure.step("Изменение задачи с не валидными данными в name"):
            for invalid_name in invalid_data:
                if invalid_name is None:
                    continue
                required_field["name"] = invalid_name
                invalid_task = auth_sess.update_task(task_id, required_field)
                assert invalid_task.status_code == 400

    def test_description_field_create_update_task(self, auth_sess, get_gen_data, get_gen_req_field):
        description_field = {"name": get_gen_data.name, "description": get_gen_data.description}

        valid_data = ["!@#$%^&*()_+{}[]':;?></.,-=`~",
            "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ", "1234567890",
            "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", "F" * 262144]
        unsaved_data = [None, 1, True]
        invalid_description = "w" * 262145

        with allure.step("Создание задачи с валидными данными в description"):
            for valid_description in valid_data:
                description_field["description"] = valid_description
                valid_task_cr = auth_sess.create_task(description_field)
                assert valid_task_cr.status_code == 200
                assert valid_task_cr.json()["description"] == valid_description

        with allure.step("Создание задачи с игнорируемыми данными в description"):
            for unsaved_description in unsaved_data:
                description_field["description"] = unsaved_description
                unsaved_description_task_cr = auth_sess.create_task(description_field)
                assert unsaved_description_task_cr.status_code == 200
                assert unsaved_description_task_cr.json()["description"] == ""

        with allure.step("Создание задачи с не валидными данными в description"):
            description_field["description"] = invalid_description
            invalid_task_cr = auth_sess.create_task(description_field)
            assert invalid_task_cr.status_code == 413  # {"err": "Task description is too long","ECODE": "TASK_014"}
            assert invalid_task_cr.json()["err"] == "Task description is too long"

        task_id = valid_task_cr.json()["id"]

        with allure.step("Изменение задачи с валидными данными в description"):
            for valid_description in valid_data:
                description_field["description"] = valid_description
                valid_task_upd = auth_sess.update_task(task_id, description_field)
                assert valid_task_upd.status_code == 200
                assert valid_task_upd.json()["description"] == valid_description

        with allure.step("Изменение задачи с игнорируемыми данными в description"):
            for unsaved_description in unsaved_data:
                description_field["description"] = unsaved_description
                unsaved_description_task_upd = auth_sess.update_task(task_id, description_field)
                assert unsaved_description_task_upd.status_code == 200

        with allure.step("Изменение задачи с не валидными данными в description"):
            description_field["description"] = invalid_description
            invalid_task_upd = auth_sess.update_task(task_id, description_field)
            assert invalid_task_upd.status_code == 413
            assert invalid_task_upd.json()["err"] == "Task description is too long"

    def test_assignees_field_create_update_task(self, auth_sess, get_gen_data, get_gen_req_field):
        assignees_field = {"name": get_gen_data.name, "assignees": get_gen_data.assignees}

        unsaved_data_cr = [[2147483647], [0], None, 1, True, ["str"], "xx", [True]]
        unsaved_data_upd = [None, False]
        invalid_assignees_cr = [2147483648]
        invalid_assignees_upd_map = [
            [[2147483647], "All assignees must have access to this task", 400],
            [["str"], "Assignees list invalid", 400],
            [[2147483648], "Internal Server Error", 500],
            ["xx", "Internal Server Error", 500],
            [[True], "Internal Server Error", 500]
        ]

        with allure.step("Создание задачи с игнорируемыми данными в assignees"):
            for unsaved_assignees in unsaved_data_cr:
                assignees_field["assignees"] = unsaved_assignees
                unsaved_assignees_task_cr = auth_sess.create_task(assignees_field)
                assert unsaved_assignees_task_cr.status_code == 200
                assert unsaved_assignees_task_cr.json()["assignees"] == []

        with allure.step("Создание задачи с не валидными данными в assignees"):
            assignees_field["assignees"] = invalid_assignees_cr
            invalid_task_cr = auth_sess.create_task(assignees_field)
            assert invalid_task_cr.status_code == 400
            assert invalid_task_cr.json()["err"] == "Invalid assignee ID. Must be a valid integer."

        task_id = unsaved_assignees_task_cr.json()["id"]

        with allure.step("Изменение задачи с игнорируемыми данными в assignees"):
            for unsaved_assignees in unsaved_data_upd:
                assignees_field["assignees"] = {"add": unsaved_assignees}
                unsaved_assignees_task_cr = auth_sess.update_task(task_id, assignees_field)
                assert unsaved_assignees_task_cr.status_code == 200
                assert unsaved_assignees_task_cr.json()["assignees"] == []

        with allure.step("Изменение задачи с не валидными данными в assignees"):
            for invalid_assignees_upd_case in invalid_assignees_upd_map:
                invalid_value = invalid_assignees_upd_case[0]
                err_msg = invalid_assignees_upd_case[1]
                expected_status = invalid_assignees_upd_case[2]

                assignees_field["assignees"] = {"add": invalid_value}

                invalid_task_cr = auth_sess.update_task(task_id, assignees_field)
                assert invalid_task_cr.status_code == expected_status
                assert invalid_task_cr.json()["err"] == err_msg

    def test_archived_field_create_update_task(self, auth_sess, get_gen_data, get_gen_req_field):
        archived_field = {"name": get_gen_data.name, "archived": get_gen_data.archived}

        valid_data = [True, False]
        unsaved_data = [2147483648, "str", [0], ["str"], [True]]

        with allure.step("Создание задачи с валидными данными в archived"):
            for valid_archived in valid_data:
                archived_field["archived"] = valid_archived
                valid_task = auth_sess.create_task(archived_field)
                assert valid_task.status_code == 200
                assert valid_task.json()["archived"] == valid_archived

        with allure.step("Создание задачи с игнорируемыми данными в archived"):
            for unsaved_archived in unsaved_data:
                archived_field["archived"] = unsaved_archived
                unsaved_assignees_task_cr = auth_sess.create_task(archived_field)
                assert unsaved_assignees_task_cr.status_code == 200
                assert unsaved_assignees_task_cr.json()["archived"] == False

        task_id = unsaved_assignees_task_cr.json()["id"]

        with allure.step("Создание задачи с валидными данными в archived"):
            for valid_archived in valid_data:
                archived_field["archived"] = valid_archived
                valid_task = auth_sess.update_task(task_id, archived_field)
                assert valid_task.status_code == 200
                assert valid_task.json()["archived"] == valid_archived

        with allure.step("Создание задачи с игнорируемыми данными в archived"):
            for unsaved_archived in unsaved_data:
                archived_field["archived"] = unsaved_archived
                unsaved_assignees_task_cr = auth_sess.update_task(task_id, archived_field)
                assert unsaved_assignees_task_cr.status_code == 500
                assert unsaved_assignees_task_cr.json()["err"] == "Internal Server Error"

    def test_tags_field_create_task(self, auth_sess, get_gen_data, get_gen_req_field):
        tags_field = {"name": get_gen_data.name, "tags": get_gen_data.tags}

        valid_data = [["!@#$%^&*()_+{}[]':;?></.,-=`~"],
            ["йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"],
            ["1234567890"], ["qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"],
            ["T" * 100]]
        unsaved_data = [2147483648, "str", True]
        invalid_data_map = [
            [["F" * 101], "Tag(s) are not valid"],
            [[0], "Invalid tag format"],
            [[True], "Invalid tag format"]
        ]

        with allure.step("Создание задачи с валидными данными в tags"):
            for valid_tags in valid_data:
                tags_field["tags"] = valid_tags
                valid_task = auth_sess.create_task(tags_field)
                assert valid_task.status_code == 200
                assert valid_task.json()["tags"][0]["name"] == valid_tags[0].lower()

        with allure.step("Создание задачи с игнорируемыми данными в tags"):
            for unsaved_tags in unsaved_data:
                tags_field["tags"] = unsaved_tags
                unsaved_assignees_task_cr = auth_sess.create_task(tags_field)
                assert unsaved_assignees_task_cr.status_code == 200
                assert unsaved_assignees_task_cr.json()["tags"] == []

        with allure.step("Создание задачи с не валидными данными в tags"):
            for invalid_case in invalid_data_map:
                value = invalid_case[0]
                err_msg = invalid_case[1]

                tags_field["tags"] = value
                invalid_task = auth_sess.create_task(tags_field)
                assert invalid_task.status_code == 400
                assert invalid_task.json()["err"] == err_msg

    def test_status_field_create_update_task(self, auth_sess, get_gen_data, get_gen_req_field):
        status_field = {"name": get_gen_data.name, "status": get_gen_data.status}
        valid_data = ["TO DO", "In Progress", "Ready to start Testing", "Testing", "Ready to Deploy", "Done", "Blocked"]
        invalid_data_map_cr = [
            [["str"], "Status must be a string", 400],
            [2147483647, "Status must be a string", 400],
            [True, "Status must be a string", 400],
            ["str", "Status not found", 400],
            ["T" * 4194248, "request entity too large", 413],
            [[0], "Status must be a string", 400],
            [[False], "Status must be a string", 400]
        ]
        invalid_data_map_upd = [
            [["str"], "Task status invalid", 400],
            [2147483647, "Task status invalid", 400],
            [True, "Task status invalid", 400],
            ["str", "Status does not exist", 400],
            ["T" * 4194248, "request entity too large", 413],
            [[0], "Task status invalid", 400],
            [[False], "Task status invalid", 400]
        ]

        with allure.step("Создание задачи с валидными данными в status"):
            for valid_status in valid_data:
                status_field["status"] = valid_status
                valid_task = auth_sess.create_task(status_field)
                assert valid_task.status_code == 200
                assert valid_task.json()["status"]["status"] == valid_status.lower()

        with allure.step("Создание задачи с не валидными данными в status"):
            for invalid_case in invalid_data_map_cr:
                value = invalid_case[0]
                err_msg = invalid_case[1]
                status_code = invalid_case[2]

                status_field["status"] = value
                invalid_task = auth_sess.create_task(status_field)
                assert invalid_task.status_code == status_code
                assert invalid_task.json()["err"] == err_msg

        task_id = valid_task.json()["id"]

        with allure.step("Создание задачи с валидными данными в status"):
            for valid_status in valid_data:
                status_field["status"] = valid_status
                valid_task = auth_sess.update_task(task_id, status_field)
                assert valid_task.status_code == 200
                assert valid_task.json()["status"]["status"] == valid_status.lower()

        with allure.step("Создание задачи с не валидными данными в status"):
            for invalid_case in invalid_data_map_upd:
                value = invalid_case[0]
                err_msg = invalid_case[1]
                status_code = invalid_case[2]

                status_field["status"] = value
                invalid_task = auth_sess.update_task(task_id, status_field)
                assert invalid_task.status_code == status_code
                assert invalid_task.json()["err"] == err_msg

    def test_date_fields_create_update_task(self, auth_sess, get_gen_data, get_gen_req_field):
        status_field = {"name": get_gen_data.name, "start_date": get_gen_data.start_date, "due_date": get_gen_data.due_date}
        valid_data = [Helper.timestamp_conv("12/31/5000"), "In Progress", "Ready to start Testing", "Testing", "Ready to Deploy", "Done", "Blocked"]
        invalid_data_map_cr = [
            [["str"], "Status must be a string", 400],
            [2147483647, "Status must be a string", 400],
            [True, "Status must be a string", 400],
            ["str", "Status not found", 400],
            ["T" * 4194248, "request entity too large", 413],
            [[0], "Status must be a string", 400],
            [[False], "Status must be a string", 400]
        ]
        invalid_data_map_upd = [
            [["str"], "Task status invalid", 400],
            [2147483647, "Task status invalid", 400],
            [True, "Task status invalid", 400],
            ["str", "Status does not exist", 400],
            ["T" * 4194248, "request entity too large", 413],
            [[0], "Task status invalid", 400],
            [[False], "Task status invalid", 400]
        ]

        with allure.step("Создание задачи с валидными данными в status"):
            for valid_status in valid_data:
                status_field["status"] = valid_status
                valid_task = auth_sess.create_task(status_field)
                assert valid_task.status_code == 200
                assert valid_task.json()["status"]["status"] == valid_status.lower()

        with allure.step("Создание задачи с не валидными данными в status"):
            for invalid_case in invalid_data_map_cr:
                value = invalid_case[0]
                err_msg = invalid_case[1]
                status_code = invalid_case[2]

                status_field["status"] = value
                invalid_task = auth_sess.create_task(status_field)
                assert invalid_task.status_code == status_code
                assert invalid_task.json()["err"] == err_msg

        task_id = valid_task.json()["id"]

        with allure.step("Создание задачи с валидными данными в status"):
            for valid_status in valid_data:
                status_field["status"] = valid_status
                valid_task = auth_sess.update_task(task_id, status_field)
                assert valid_task.status_code == 200
                assert valid_task.json()["status"]["status"] == valid_status.lower()

        with allure.step("Создание задачи с не валидными данными в status"):
            for invalid_case in invalid_data_map_upd:
                value = invalid_case[0]
                err_msg = invalid_case[1]
                status_code = invalid_case[2]

                status_field["status"] = value
                invalid_task = auth_sess.update_task(task_id, status_field)
                assert invalid_task.status_code == status_code
                assert invalid_task.json()["err"] == err_msg
