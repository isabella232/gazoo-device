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

"""Test suite for all auxiliary devices, covers basic functionality."""
import os
import shutil
import time
from typing import Tuple, Type

import gazoo_device
from gazoo_device import fire_manager
from gazoo_device.base_classes import auxiliary_device
from gazoo_device.tests.functional_tests.utils import gdm_test_base


class AuxiliaryDeviceCommonTestSuite(gdm_test_base.GDMTestBase):
  """Common test suite for all auxiliary devices."""

  @classmethod
  def is_applicable_to(cls, device_type: str,
                       device_class: Type[gdm_test_base.DeviceType],
                       device_name: str) -> bool:
    """Determine if this test suite can run on the given device."""
    return issubclass(device_class, auxiliary_device.AuxiliaryDevice)

  @classmethod
  def requires_pairing(cls) -> bool:
    """Returns True if the device must be paired to run this test suite."""
    return False

  @classmethod
  def required_test_config_variables(cls) -> Tuple[str, ...]:
    """Returns keys required to be present in the functional test config."""
    return ("shell_cmd",)

  def test_close_device(self):
    """Tests that device.close() stops logging."""
    log_file = self.device.log_file_name
    self.assertTrue(
        os.path.exists(log_file), "Cannot test close as device is not logging")
    self.device.close()
    time.sleep(1)
    size = os.stat(log_file).st_size
    time.sleep(.1)
    self.assertEqual(size, os.stat(log_file).st_size,
                     "Log has updated after device is closed")

  def test_logging(self):
    """Tests that device logs are being captured."""
    log_file = self.device.log_file_name
    self.assertTrue(os.path.exists(log_file),
                    f"{self.device.name}'s log file {log_file} does not exist")
    self.assertTrue(os.path.getsize(log_file),
                    f"{self.device.name}'s log file {log_file} is empty")

  def test_serial_number(self):
    """Tests retrieval of 'serial_number' property."""
    serial_number = self.device.serial_number
    self.assertTrue(serial_number)
    self.assertIsInstance(serial_number, str)

  def test_firmware_version(self):
    """Tests retrieval of 'firmware_version' property."""
    if not hasattr(type(self.device), "firmware_version"):
      self.skipTest(
          f"{self.device.device_type} does not implement firmware_version")

    firmware_version = self.device.firmware_version
    self.assertTrue(firmware_version)
    self.assertIsInstance(firmware_version, str)

  def test_reboot(self):
    """Tests rebooting the device and verifies it's online after."""
    if not hasattr(type(self.device), "reboot"):
      self.skipTest(f"{self.device.device_type} does not implement reboot()")

    self.device.reboot()
    self.assertTrue(
        self.device.connected,
        f"{self.device.name} is offline after reboot() execution finished. "
        "reboot should block until the device comes back online and becomes "
        "responsive.")

  def test_factory_reset(self):
    """Tests factory resetting the device and verifies it's online after."""
    if not hasattr(type(self.device), "factory_reset"):
      self.skipTest(
          f"{self.device.device_type} does not implement factory_reset()")

    self.device.factory_reset()
    self.assertTrue(
        self.device.connected,
        f"{self.device.name} is offline after factory_reset() execution "
        "finished. factory_reset should block until the device comes back "
        "online and becomes responsive.")

  def test_shell(self):
    """Tests shell() method."""
    if not hasattr(type(self.device), "shell"):
      self.skipTest(f"{self.device.device_type} does not implement shell()")

    response = self.device.shell(self.test_config["shell_cmd"])
    self.assertTrue(response)
    self.assertIsInstance(response, str)

  def test_get_prop(self):
    """Tests that FireManager.get_prop() can retrieve all properties."""
    device_name = self.device.name
    self.device.close()
    fire_manager_instance = fire_manager.FireManager()
    try:
      fire_manager_instance.get_prop(device_name)
    finally:
      fire_manager_instance.close()

  def test_redetect(self):
    """Tests device detection and properties populated during detection."""
    self.device.close()
    time.sleep(.2)
    new_file_devices_name = os.path.join(self.get_output_dir(),
                                         "test_redetect_devices.json")
    new_file_options_name = os.path.join(self.get_output_dir(),
                                         "test_redetect_device_options.json")
    new_log_file = os.path.join(self.get_output_dir(), "test_redetect_gdm.txt")

    shutil.copy(self.get_manager().device_file_name, new_file_devices_name)
    shutil.copy(self.get_manager().device_options_file_name,
                new_file_options_name)
    new_manager = gazoo_device.Manager(
        device_file_name=new_file_devices_name,
        device_options_file_name=new_file_options_name,
        log_directory=self.get_output_dir(),
        gdm_log_file=new_log_file)
    try:
      new_manager.redetect(self.device.name, self.get_output_dir())
    finally:
      new_manager.close()

    self.assertTrue(
        self.device.name in new_manager.other_devices,
        "Device was not successfully detected. See test_redetect_gdm.txt and "
        f"{self.device.device_type}_detect.txt for more info")
    old_dict = self.get_manager().other_devices[self.device.name]["persistent"]
    new_dict = new_manager.other_devices[self.device.name]["persistent"]

    for name, a_dict in [("Old", old_dict), ("Detected", new_dict)]:
      self.logger.info("%s configuration:", name)
      for key, value in a_dict.items():
        self.logger.info("\t%s:%s", key, value)

    missing_props = []
    bad_values = []
    for prop, old_value in old_dict.items():
      if prop in new_dict:
        new_value = new_dict[prop]
        if old_value != new_value:
          bad_values.append("{}: {!r} was previously {!r}".format(
              prop, new_value, old_value))
      else:
        missing_props.append(prop)
    msg = ""
    if missing_props:
      msg += "{} is missing the following previous props: {}.\n".format(
          self.device.name, missing_props)
    if bad_values:
      msg += "{} has the following mismatched values: {}.".format(
          self.device.name, ", ".join(bad_values))

    self.assertFalse(missing_props or bad_values, msg)


if __name__ == "__main__":
  gdm_test_base.main()
