def clear_board(auth_sess, *ids):
    for task_id in ids:
        assert auth_sess.delete_task(task_id).status_code == 204
