from SecureVision.source.backend.database.user import User, register_users, login_user


class TestRegistration:

    @staticmethod
    def cleanup(base_obj, engine):
        base_obj.metadata.drop_all(engine)

    def test_register_users(self, register_data):
        # Setup
        session_obj, base_created, engine, desired, json_path = register_data
        # Exercise
        register_users(session_obj, json_path)
        in_db_names = [user.name for user in session_obj.query(User).order_by(User.id)]
        # Verify
        assert in_db_names == desired
        # Cleanup
        TestRegistration.cleanup(base_created, engine)


class TestLogin:

    @staticmethod
    def cleanup(base_obj, engine):
        base_obj.metadata.drop_all(engine)

    def test_register_users(self, register_data):
        # Setup
        session_obj, base_created, engine, desired, json_path = register_data
        # Exercise
        register_users(session_obj, json_path)
        in_db_names = [user.name for user in session_obj.query(User).order_by(User.id)]
        # Verify
        assert in_db_names == desired
        # Cleanup
        TestRegistration.cleanup(base_created, engine)
