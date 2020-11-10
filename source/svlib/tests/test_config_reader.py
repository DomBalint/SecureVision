import os
import sys

sys.path.append('..')

from config_reader import ConfigReader


class TestConfigReader:

    def test_list_config_files(self, desired_config_files):
        # Setup
        config_directory = os.path.join(os.getcwd(), 'data_test')
        # Exercise
        actual_config_files = ConfigReader.list_config_files(config_directory)
        # Verify
        assert desired_config_files == actual_config_files

    def test_parse_yaml(self, desired_configs):
        # Setup
        file, desired_conf = desired_configs
        path_config = os.path.join(os.getcwd(), 'data_test', file)
        # Exercise
        actual_conf = ConfigReader.parse_yaml(path_config)
        # Verify
        assert desired_conf == actual_conf

    def test_get(self, whole_config):
        # Setup
        desired_conf = whole_config
        # Exercise
        cr = ConfigReader('data_test')
        actual_conf = cr.svt_config
        # Verify
        assert desired_conf == actual_conf
        assert cr.get('sql_alchemy') == desired_conf['sql_alchemy']
        assert cr.get('sql_alchemy', 'host') == desired_conf['sql_alchemy']['host']
        assert cr.get('sql_alchemy', 'port') == desired_conf['sql_alchemy']['port']
