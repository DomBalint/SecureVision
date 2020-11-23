import os

import pytest
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

    @pytest.mark.parametrize('user_data', [('Guard1', 'Guard1', 'Guard1pass'),
                                           ('Guard3', 'Guard3', 'Guard3pass'),
                                           ('GuardNone', 'None', 'None')], indirect=['user_data'])
    def test_login_user(self, user_data):
        # Setup
        user_handler_instance, base_created, engine, session_obj, desired, name, pass_desired = user_data
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

    @pytest.mark.parametrize('user_data', [('Guard1', 1, None)], indirect=['user_data'])
    def test_user_fb(self, user_data):
        # Setup
        user_handler_instance, base_created, engine, session_obj, desired, name, _ = user_data
        # Exercise
        user_handler_instance.user_fb_update_by_name(name)
        user = user_handler_instance.user_by_name(name)
        # Verify
        assert user.num_feedback == desired
        # Cleanup
        user_handler_instance.release_resources()
        cleanup(base_created, engine)


class TestCameraTable:

    @pytest.mark.parametrize('cam_all', [[1, 2, 3]], indirect=['cam_all'])
    def test_add_camera(self, cam_all):
        # Setup
        cam_handler_instance, base_created, engine, session_obj, desired = cam_all
        # Exercise
        cam_handler_instance.add_camera()
        cam_handler_instance.add_camera()
        cam_handler_instance.add_camera()
        cams = cam_handler_instance.all_cams()
        cams_ids = [cam.id for cam in cams]
        assert cams_ids == desired
        # Cleanup
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)

    @pytest.mark.parametrize('cam_all', [([1, 3], 2)], indirect=['cam_all'])
    def test_delete_camera(self, cam_all):
        # Setup
        cam_handler_instance, base_created, engine, session_obj, desired = cam_all
        # Exercise
        cam_handler_instance.add_camera()
        cam_handler_instance.add_camera()
        cam_handler_instance.add_camera()
        cam_handler_instance.cam_delete(desired[1])
        cams = cam_handler_instance.all_cams()
        cams_ids = [cam.id for cam in cams]
        assert cams_ids == desired[0]
        # Cleanup
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)

    @pytest.mark.parametrize('cam_all', [[1, True], [2, False]], indirect=['cam_all'])
    def test_start_camera(self, cam_all):
        # Setup
        cam_handler_instance, base_created, engine, session_obj, desired = cam_all
        # Exercise
        cam_handler_instance.add_camera()
        started = cam_handler_instance.update_start_camera(desired[0])
        cam = cam_handler_instance.cam_by_id(desired[0])
        assert started == desired[1]
        if started:
            assert cam.is_running == desired[1]
        # Cleanup
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)

    @pytest.mark.parametrize('cam_all', [[1, True], [2, False]], indirect=['cam_all'])
    def test_stop_camera(self, cam_all):

        # Setup
        cam_handler_instance, base_created, engine, session_obj, desired = cam_all
        # Exercise
        cam_handler_instance.add_camera()
        # Camera has to be started in order to be stopped
        cam_handler_instance.update_start_camera(desired[0])
        stopped = cam_handler_instance.update_stop_camera(desired[0])
        cam = cam_handler_instance.cam_by_id(desired[0])
        assert stopped == desired[1]
        if stopped:
            assert cam.is_running != desired[1]
        # Cleanup
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)


class TestImageTable:

    @pytest.mark.parametrize('img_all', [('test_url1', 1)], indirect=['img_all'])
    def test_add_img(self, img_all):
        # Setup
        img_handler_instance, cam_handler_instance, base_created, engine, session_obj, desired = img_all
        # Exercise
        cam_handler_instance.add_camera()
        img_handler_instance.add_image(desired[0], desired[1])
        img = img_handler_instance.img_by_path(desired[0])
        assert img.img_path == desired[0]
        # Cleanup
        img_handler_instance.release_resources()
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)

    @pytest.mark.parametrize('img_all', [('test_url1', 1, 'new_name')], indirect=['img_all'])
    def test_update_img(self, img_all):
        # Setup
        img_handler_instance, cam_handler_instance, base_created, engine, session_obj, desired = img_all
        # Exercise
        cam_handler_instance.add_camera()
        img_handler_instance.add_image(desired[0], desired[1])
        img = img_handler_instance.img_by_path(desired[0])
        assert img.img_path == desired[0]
        img_handler_instance.update_image_by_path('test_url1', 'new_name')
        img = img_handler_instance.img_by_path('new_name')
        assert img.img_path == desired[2]
        # Cleanup
        img_handler_instance.release_resources()
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)


class TestFeedbackTable:

    @pytest.mark.parametrize('fb_all', [('test_url1', 1, 1, 1, True)], indirect=['fb_all'])
    def test_add_fb(self, fb_all):
        # Setup
        img_handler_instance, fb_handler_instance, cam_handler_instance, base_created, engine, session_obj, desired = fb_all
        # Exercise
        cam_handler_instance.add_camera()
        img_handler_instance.add_image(desired[0], desired[1])
        fb_handler_instance.add_fb(desired[2], desired[3])
        fb = fb_handler_instance.fb_by_img_id(desired[2])
        assert fb.correct_detection == desired[-1]
        # Cleanup
        img_handler_instance.release_resources()
        fb_handler_instance.release_resources()
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)

    @pytest.mark.parametrize('fb_all', [(1, True, False)], indirect=['fb_all'])
    def test_update_fb(self, fb_all):
        # Setup
        img_handler_instance, fb_handler_instance, cam_handler_instance, base_created, engine, session_obj, desired = fb_all
        # Exercise
        cam_handler_instance.add_camera()
        img_handler_instance.add_image('test_url1', 1)
        fb_handler_instance.add_fb(desired[0], desired[1])
        fb = fb_handler_instance.fb_by_img_id(1)
        assert fb.correct_detection == desired[desired[1]]
        fb_handler_instance.update_fb_by_fb_id(1, False)
        assert fb.correct_detection == desired[-1]
        # Cleanup
        img_handler_instance.release_resources()
        fb_handler_instance.release_resources()
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)


class TestAnnotationTable:

    @pytest.mark.parametrize('ann_all', [['Knife', 'Gun', 'Gun']], indirect=['ann_all'])
    def test_add_ann(self, ann_all):
        # Setup
        img_handler_instance, cam_handler_instance, ann_handler_instance, base_created, engine, session_obj, desired = ann_all
        # Exercise
        cam_handler_instance.add_camera()
        img_handler_instance.add_image('test_url1', 1)
        ann_handler_instance.add_annotations_from_path(os.path.join(os.getcwd(), 'data_test', 'test_annotations.json'))
        anns = ann_handler_instance.anns_by_img_id(1)
        ann_types = [ann.obj_type for ann in anns]
        assert ann_types == desired
        # Cleanup
        img_handler_instance.release_resources()
        ann_handler_instance.release_resources()
        cam_handler_instance.release_resources()
        cleanup(base_created, engine)
