from SecureVision.source.backend.database.user import User


def cleanup(base_obj, engine):
    base_obj.metadata.drop_all(engine)


class TestRegistration:

    def test_register_users(self, register_data):
        # Setup
        user_handler_instance, base_created, engine, session_obj, desired, json_path = register_data
        # Exercise
        user_handler_instance.register_users_unique(json_path)
        in_db_names = [user.name for user in session_obj.query(User).order_by(User.id)]
        # Verify
        assert in_db_names == desired
        # Cleanup
        cleanup(base_created, engine)


class TestLogin:

    def test_login_user(self, login_data):
        # Setup
        user_handler_instance, base_created, engine, session_obj, desired, name = login_data
        # Exercise
        user = user_handler_instance.user_by_name(name)
        if user:
            user_name = user.name
        else:
            user_name = 'None'
        # Verify
        assert user_name == desired
        # Cleanup
        cleanup(base_created, engine)
