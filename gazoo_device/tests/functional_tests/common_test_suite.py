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

"""Test suite for all primary devices. Covers basic functionality."""
import datetime
import os
import shutil
import time
from typing import Tuple, Type

import gazoo_device
from gazoo_device import errors
from gazoo_device import fire_manager
from gazoo_device.base_classes import gazoo_device_base
from gazoo_device.tests.functional_tests.utils import gdm_test_base
import retry

# Allows the log process to catch up after device creation using time.sleep().
# Prevents _verify_no_unexpected_bootups() from checking old bootup log events.
_LOG_CATCH_UP_DELAY = 3


class CommonTestSuite(gdm_test_base.GDMTestBase):
  """Common test suite for all primary devices."""

  @classmethod
  def is_applicable_to(cls, device_type: str,
                       device_class: Type[gdm_test_base.DeviceType],
                       device_name: str) -> bool:
    """Determine if this test suite can run on the given device."""
    return issubclass(device_class, gazoo_device_base.GazooDeviceBase)

  @classmethod
  def requires_pairing(cls) -> bool:
    """Returns True if the device must be paired to run this test suite."""
    return False

  @classmethod
  def required_test_config_variables(cls) -> Tuple[str, ...]:
    """Returns keys required to be present in the functional test config."""
    return ("shell_cmd", "expect", "known_logline")

  @retry.retry(tries=2, delay=30)
  def test_01_factory_reset(self):
    """Tests factory resetting the device and verifies it's online after.

    The test name includes "01" to make sure this test appears (and therefore
    runs) before other tests in alphabetic order.
    """
    time.sleep(_LOG_CATCH_UP_DELAY)
    start_time = datetime.datetime.now()

    self.device.factory_reset()
    self.assertTrue(
        self.device.connected,
        f"{self.device.name} is offline after factory_reset() execution "
        "finished. factory_reset should block until the device comes back "
        "online and becomes responsive.")
    self._verify_no_unexpected_reboots(start_time)

  def test_close_device(self):
    """Tests that device.close() stops logging."""
    log_file = self.device.log_file_name
    self.assertTrue(
        os.path.exists(log_file), "Cannot test close as device is not logging")
    self.device.close()
    time.sleep(1)
    size = os.stat(log_file).st_size
    time.sleep(.1)
    self.assertEqual(size,
                     os.stat(log_file).st_size,
                     "Log has updated after device is closed")

  def test_logging(self):
    """Tests that device logs are being captured."""
    self._verify_logging()

  def test_serial_number(self):
    """Tests retrieval of 'serial_number' property."""
    serial_number = self.device.serial_number
    self.assertTrue(serial_number)
    self.assertIsInstance(serial_number, str)

  def test_firmware_version(self):
    """Tests retrieval of 'firmware_version' property."""
    self._verify_firmware_version()

  @retry.retry(tries=2, delay=30)
  def test_reboot_and_expect_known_logline(self):
    """Tests rebooting and waiting for a certain log line.

    After the reboot verifies that the device is connected, logging, able to
    retrieve the firmware version, passes health checks, that the device
    actually rebooted, and that no unexpected bootups happened. Also waits for
    the known log line after rebooting.
    """
    time.sleep(_LOG_CATCH_UP_DELAY)
    start_time = datetime.datetime.now()

    self.device.reboot()
    self.assertTrue(
        self.device.connected,
        f"{self.device.name} is offline after reboot() execution finished. "
        "reboot should block until the device comes back online and becomes "
        "responsive.")
    self._verify_logging()
    self._verify_firmware_version()
    self._verify_expect_log()

    # Wait to ensure last bootup event has been logged by the logger process.
    time.sleep(_LOG_CATCH_UP_DELAY)
    self._verify_boot_up_log(start_time)
    self._verify_no_unexpected_reboots(start_time)

    try:
      self.device.check_device_ready()
    except errors.CheckDeviceReadyError as err:
      self.fail(
          f"{self.device.name} didn't pass health checks after reboot: {err!r}")

  def test_shell(self):
    """Tests shell() method."""
    response = self.device.shell(self.test_config["shell_cmd"])
    self.assertTrue(response)
    self.assertIsInstance(response, str)

  def test_start_new_log(self):
    """Tests that start_new_log begins a new log file."""
    old_log_file_name = self.device.log_file_name
    self.device.start_new_log(log_name_prefix=self.get_log_suffix())
    self.assertNotEqual(
        old_log_file_name, self.device.log_file_name,
        f"Expected log file name to change from {old_log_file_name}")
    self.assertTrue(
        os.path.exists(old_log_file_name),
        f"Expected old log file name {old_log_file_name} to exist")
    self.assertTrue(
        os.path.exists(self.device.log_file_name),
        f"Expected new log file name {self.device.log_file_name} to exist")

  def test_get_prop(self):
    """Tests that FireManager.get_prop() can retrieve all properties."""
    device_name = self.device.name
    self.device.close()
    fire_manager_instance = fire_manager.FireManager()
    try:
      fire_manager_instance.get_prop(device_name)
    finally:
      fire_manager_instance.close()

  @retry.retry(tries=2, delay=30)
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

    # pylint: disable=protected-access
    self.assertTrue(
        self.device.name in new_manager._devices,
        "Device was not successfully detected. See test_redetect_gdm.txt and "
        f"{self.device.device_type}_detect.txt for more info")
    old_dict = self.get_manager()._devices[self.device.name]["persistent"]
    new_dict = new_manager._devices[self.device.name]["persistent"]
    # pylint: enable=protected-access

    for name, a_dict in [("Old", old_dict), ("Detected", new_dict)]:
      self.logger.info("%s configuration:", name)
      for key, value in a_dict.items():
        self.logger.info("\t%s: %s", key, value)

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

  def _verify_firmware_version(self):
    """Verifies that firmware version is a non-empty string."""
    firmware_version = self.device.firmware_version
    self.assertTrue(firmware_version)
    self.assertIsInstance(firmware_version, str)

  def _verify_logging(self):
    """Verifies that the device has a non-empty log file."""
    log_file = self.device.log_file_name
    self.assertTrue(os.path.exists(log_file),
                    f"{self.device.name}'s log file {log_file} does not exist")
    self.assertTrue(os.path.getsize(log_file),
                    f"{self.device.name}'s log file {log_file} is empty")

  def _verify_boot_up_log(self, start_time):
    """Verifies that the device booted up once after the start_time."""
    parser_result = self.device.event_parser.get_last_event(["basic.bootup"])
    self.assertGreater(parser_result.count, 0,
                       "Error: event label 'basic.bootup' not found.")
    timestamp = parser_result.results_list[0]["system_timestamp"]
    self.assertGreater(
        timestamp, start_time,
        "Expected basic bootup timestamp {} to be > start time {}".format(
            timestamp, start_time))

  def _verify_expect_log(self):
    """Verifies that 'known_logline' occurs in device logs."""
    self.logger.info("Expecting logline %r", self.test_config["known_logline"])
    res = self.device.switchboard.expect([self.test_config["known_logline"]],
                                         timeout=30)
    self.assertFalse(
        res.timedout,
        "Expect timed out when waiting for log line {!r}. Shell response: {}"
        .format(self.test_config["known_logline"], res.before))

  def _verify_no_unexpected_reboots(self, start_time):
    """Verifies that no unexpected reboots occurred after start_time."""
    bootups = self.device.event_parser.get_unexpected_reboots()
    unexpected_timestamps = [event["system_timestamp"]
                             for event in bootups
                             if event["system_timestamp"] > start_time]
    self.assertFalse(
        unexpected_timestamps,
        "There were {} unexpected bootups after {} at {}".format(
            len(unexpected_timestamps), start_time, unexpected_timestamps))


if __name__ == "__main__":
  gdm_test_base.main()
