# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for gazoo_device.utility.host_utils.py."""
import os
import unittest
from unittest import mock

from gazoo_device import config
from gazoo_device import data_types
from gazoo_device import extensions
from gazoo_device.utility import host_utils
import immutabledict

_TEST_PACKAGE = "foo_package"
_EXPECTED_KEY_DIR = os.path.join(config.KEYS_DIRECTORY, _TEST_PACKAGE)
_TEST_KEY_SSH_PRIVATE_NAME = "foo_key"
_EXPECTED_KEY_SSH_PRIVATE_PATH = os.path.join(_EXPECTED_KEY_DIR,
                                              _TEST_KEY_SSH_PRIVATE_NAME)
_TEST_KEY_SSH_PUBLIC_NAME = "foo_key.pub"
_EXPECTED_KEY_SSH_PUBLIC_PATH = os.path.join(_EXPECTED_KEY_DIR,
                                             _TEST_KEY_SSH_PUBLIC_NAME)
_TEST_KEY_OTHER_NAME = "bar_key"
_EXPECTED_KEY_OTHER_PATH = os.path.join(_EXPECTED_KEY_DIR, _TEST_KEY_OTHER_NAME)
_TEST_KEY_SSH_PRIVATE = data_types.KeyInfo(
    _TEST_KEY_SSH_PRIVATE_NAME, type=data_types.KeyType.SSH,
    package=_TEST_PACKAGE)
_TEST_KEY_SSH_PUBLIC = data_types.KeyInfo(
    _TEST_KEY_SSH_PUBLIC_NAME, type=data_types.KeyType.SSH,
    package=_TEST_PACKAGE)
_TEST_KEY_OTHER = data_types.KeyInfo(
    _TEST_KEY_OTHER_NAME, type=data_types.KeyType.OTHER, package=_TEST_PACKAGE)


class HostUtilsTests(unittest.TestCase):
  """Unit tests for gazoo_device.utility.host_utils.py."""

  def setUp(self):
    super().setUp()

    self.mock_download_key = mock.Mock()
    extensions_keys_patch = mock.patch.object(
        extensions, "keys", new=[_TEST_KEY_SSH_PRIVATE, _TEST_KEY_OTHER])
    extensions_keys_patch.start()
    self.addCleanup(extensions_keys_patch.stop)
    package_info_patch = mock.patch.object(
        extensions, "package_info", new={
            _TEST_PACKAGE: immutabledict.immutabledict({
                "version": "0.0.1",
                "key_download_function": self.mock_download_key,
            })
        })
    package_info_patch.start()
    self.addCleanup(package_info_patch.stop)

  def test_get_key_path(self):
    """Test that path returned by get_key_path() is correct."""
    self.assertEqual(host_utils.get_key_path(_TEST_KEY_SSH_PRIVATE),
                     _EXPECTED_KEY_SSH_PRIVATE_PATH)

  @mock.patch.object(os.path, "isdir", side_effect=[False, True])
  @mock.patch.object(os, "makedirs")
  @mock.patch.object(os.path, "exists", return_value=True)
  @mock.patch.object(host_utils, "_set_key_permissions")
  def test_download_key_creates_directory_if_its_absent(
      self, unused_mock_set_key_permissions, unused_mock_exists, mock_makedirs,
      mock_isdir):
    """Test that _download_key() creates package key dir if it's absent."""
    host_utils._download_key(_TEST_KEY_SSH_PRIVATE)
    mock_isdir.assert_called_once_with(_EXPECTED_KEY_DIR)
    mock_makedirs.assert_called_once_with(_EXPECTED_KEY_DIR)
    self.mock_download_key.assert_called_once_with(
        _TEST_KEY_SSH_PRIVATE, _EXPECTED_KEY_SSH_PRIVATE_PATH)

  @mock.patch.object(os.path, "isdir", return_value=True)
  @mock.patch.object(os, "makedirs")
  @mock.patch.object(os.path, "exists", return_value=True)
  @mock.patch.object(host_utils, "_set_key_permissions")
  def test_download_key_does_not_create_directory_if_its_present(
      self, unused_mock_set_key_permissions, unused_mock_exists, mock_makedirs,
      mock_isdir):
    """Test that _download_key() does not create key dir if it's present."""
    host_utils._download_key(_TEST_KEY_SSH_PRIVATE)
    mock_isdir.assert_called_once_with(_EXPECTED_KEY_DIR)
    mock_makedirs.assert_not_called()

  @mock.patch.object(os.path, "isdir", return_value=True)
  @mock.patch.object(os, "makedirs")
  @mock.patch.object(os.path, "exists", return_value=False)
  def test_download_key_raises_if_key_isnt_downloaded(
      self, mock_exists, unused_mock_makedirs, unused_mock_isdir):
    """Test that _download_key() raises an error if key isn't downloaded."""
    error_regex = r"Key .*{}.* was not downloaded to {}".format(
        _TEST_KEY_SSH_PRIVATE_NAME, _EXPECTED_KEY_SSH_PRIVATE_PATH)
    with self.assertRaisesRegex(FileNotFoundError, error_regex):
      host_utils._download_key(_TEST_KEY_SSH_PRIVATE)
    mock_exists.assert_called_once_with(_EXPECTED_KEY_SSH_PRIVATE_PATH)

  @mock.patch.object(os.path, "isdir", return_value=True)
  @mock.patch.object(os, "makedirs")
  @mock.patch.object(os.path, "exists", return_value=True)
  @mock.patch.object(host_utils, "_set_key_permissions")
  def test_download_key_sets_permissions_for_private_ssh_keys(
      self, mock_set_key_permissions, unused_mock_exists, unused_mock_makedirs,
      unused_mock_isdir):
    """Test that _download_key() changes permissions for SSH keys."""
    host_utils._download_key(_TEST_KEY_SSH_PRIVATE)
    mock_set_key_permissions.assert_called_once_with(
        _EXPECTED_KEY_SSH_PRIVATE_PATH)

  @mock.patch.object(os.path, "isdir", return_value=True)
  @mock.patch.object(os, "makedirs")
  @mock.patch.object(os.path, "exists", return_value=True)
  @mock.patch.object(host_utils, "_set_key_permissions")
  def test_download_key_doesnt_set_permissions_for_non_ssh_keys(
      self, mock_set_key_permissions, unused_mock_exists, unused_mock_makedirs,
      unused_mock_isdir):
    """Test that _download_key() doesn't change permissions for non-SSH keys."""
    host_utils._download_key(_TEST_KEY_OTHER)
    mock_set_key_permissions.assert_not_called()

  @mock.patch.object(os.path, "isdir", return_value=True)
  @mock.patch.object(os, "makedirs")
  @mock.patch.object(os.path, "exists", return_value=True)
  @mock.patch.object(host_utils, "_set_key_permissions")
  def test_download_key_doesnt_set_permissions_for_public_ssh_keys(
      self, mock_set_key_permissions, unused_mock_exists, unused_mock_mkdir,
      unused_mock_isdir):
    """Test that _download_key() doesn't set permissions for public SSH keys."""
    host_utils._download_key(_TEST_KEY_SSH_PUBLIC)
    mock_set_key_permissions.assert_not_called()

  @mock.patch.object(os, "chmod")
  def test_set_key_permissions_already_correct(self, mock_chmod):
    """Test _set_key_permissions for already correct permissions."""
    mock_stat_result = mock.Mock()
    mock_stat_result.st_mode = int("400", 8)
    with mock.patch.object(os, "stat", return_value=mock_stat_result):
      host_utils._set_key_permissions(_EXPECTED_KEY_SSH_PRIVATE_PATH)
    mock_chmod.assert_not_called()

  @mock.patch.object(os, "chmod")
  def test_set_key_permissions_incorrect_permissions(self, mock_chmod):
    """Test _set_key_permissions for incorrect permissions."""
    mock_stat_result = mock.Mock()
    mock_stat_result.st_mode = int("644", 8)
    with mock.patch.object(os, "stat", return_value=mock_stat_result):
      host_utils._set_key_permissions(_EXPECTED_KEY_SSH_PRIVATE_PATH)
    mock_chmod.assert_called_once_with(_EXPECTED_KEY_SSH_PRIVATE_PATH,
                                       int("400", 8))

  @mock.patch.object(os, "chmod", side_effect=OSError("Some failure"))
  def test_set_key_permissions_incorrect_permissions_failure(self, mock_chmod):
    """Test _set_key_permissions failing to correct permissions."""
    mock_stat_result = mock.Mock()
    mock_stat_result.st_mode = int("644", 8)
    with mock.patch.object(os, "stat", return_value=mock_stat_result):
      with self.assertRaisesRegex(ValueError, "Unable to change permissions"):
        host_utils._set_key_permissions(_EXPECTED_KEY_SSH_PRIVATE_PATH)
    mock_chmod.assert_called_once_with(_EXPECTED_KEY_SSH_PRIVATE_PATH,
                                       int("400", 8))


if __name__ == "__main__":
  unittest.main()
