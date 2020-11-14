from werkzeug.security import check_password_hash

from SecureVision.source.backend.database.user import User


def cleanup(base_obj, engine):
    base_obj.metadata.drop_all(engine)


class TestUserTable:

    def test_register_users(self, register_data):
        # Setup
        user_handler_instance, base_created, engine, session_obj, desired, json_path = register_data
        # Exercise
        user_handler_instance.register_users_unique(json_path)
        in_db_names = [user.name for user in session_obj.query(User).order_by(User.id)]
        # Verify
        assert in_db_names == desired
        # Cleanup
        user_handler_instance.release_resources()
        cleanup(base_created, engine)

    def test_login_user(self, login_data):
        # Setup
        user_handler_instance, base_created, engine, session_obj, desired, name, pass_desired = login_data
        # Exercise
        user = user_handler_instance.user_by_name(name)
        password = user_handler_instance.user_pass_by_name(name)
        if user:
            user_name = user.name
        else:
            user_name = 'None'
        # Verify
        assert user_name == desired
        if user:
            assert user.user_pass == password
            assert check_password_hash(password, pass_desired)
        # Cleanup
        user_handler_instance.release_resources()
        cleanup(base_created, engine)

    def test_user_fb(self, fb_data):
        # Setup
        user_handler_instance, base_created, engine, session_obj, desired, name = fb_data
        # Exercise
        user_handler_instance.user_fb_update_by_name(name)
        user = user_handler_instance.user_by_name(name)
        # Verify
        assert user.num_feedback == desired
        # Cleanup
        user_handler_instance.release_resources()
        cleanup(base_created, engine)