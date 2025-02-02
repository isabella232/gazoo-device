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

"""Interface for a PwRPC (Pigweed RPC) button capability."""
import abc
from gazoo_device.capabilities.interfaces import capability_base


class PwRPCButtonBase(capability_base.CapabilityBase):
  """Pigweed RPC button capability for devices communicating over PwRPC."""

  @abc.abstractmethod
  def push(self, button_id: int) -> None:
    """Push the button with the given button id.

    Args:
      button_id: Button ID.
    """
