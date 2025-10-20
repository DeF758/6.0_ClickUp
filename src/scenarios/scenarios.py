from utils.helpers import Helper


def clear_board(auth_sess, *ids):
    for task_id in ids:
        assert auth_sess.delete_task(task_id).status_code == 204


def csdc(auth_sess, field_name: str, valid_data: list, get_gen_data):
    test_field_json = Helper.choice_field(field_name, get_gen_data)
    for valid_value in valid_data:
        test_field_json[field_name] = valid_value
        valid_task = auth_sess.create_task(test_field_json)
        # assert valid_task.status_code == 200
        return valid_task


def create_task_and_get_body(auth_sess, field_name: str, get_gen_data):
    test_field_json = Helper.choice_field(field_name, get_gen_data)
    task_id = auth_sess.create_task(test_field_json)
    assert task_id.status_code == 200
    return task_id.json()["id"], test_field_json


def create_and_get_task_id(auth_sess, get_gen_data):
    task_id = auth_sess.create_task(get_gen_data)
    assert task_id.status_code == 200
    return task_id.json()["id"]


def check_cr_invalid_map(auth_sess, field_name: str, invalid_data_map: list, get_gen_data):
    test_field_json = Helper.choice_field(field_name, get_gen_data)
    for invalid_case in invalid_data_map:
        value = invalid_case[0]
        err_msg = invalid_case[1]
        status_code = invalid_case[2]
        test_field_json[field_name] = value
        invalid_task = auth_sess.create_task(test_field_json)
        assert invalid_task.status_code == status_code
        assert invalid_task.json()["err"] == err_msg


def check_upd_invalid_map(auth_sess, task_id, field_name: str, invalid_data_map: list, get_gen_data):
    test_field_json = Helper.choice_field(field_name, get_gen_data)
    for invalid_case in invalid_data_map:
        value = invalid_case[0]
        err_msg = invalid_case[1]
        status_code = invalid_case[2]
        test_field_json[field_name] = value
        invalid_task = auth_sess.update_task(task_id, test_field_json)
        assert invalid_task.status_code == status_code
        assert invalid_task.json()["err"] == err_msg
