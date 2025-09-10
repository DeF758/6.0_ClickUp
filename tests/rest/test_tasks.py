class TestTask:
    def test_create_task(self, auth_sess, get_gen_task):
        task_data = get_gen_task
        # task_data.archived = False
        first_task = auth_sess.create_task(data=task_data)
        assert first_task.status_code == 200
        auth_sess.get_task(first_task.json()["id"])

