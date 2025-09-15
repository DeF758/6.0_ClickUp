import allure


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

        req = get_gen_req_field
        assert auth_sess.create_task(data=get_gen_req_field).status_code == 200

    def test_required_field_create_update_task_(self, auth_sess, get_gen_data, get_gen_req_field):
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

        with allure.step("Создание задачи с невалидными данными в name"):
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

        with allure.step("Изменение задачи с невалидными данными в name"):
            for invalid_name in invalid_data:
                if invalid_name is None:
                    continue
                required_field["name"] = invalid_name
                invalid_task = auth_sess.update_task(task_id, required_field)
                assert invalid_task.status_code == 400
