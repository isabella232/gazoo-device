# How to Contribute to Gazoo Device Manager

This document is for you if you're interested in adding support for your
device(s) to GDM.

## Table of contents

*   [General information](#general-information)
    *   [Contributor License Agreement](#contributor-license-agreement)
    *   [Code reviews](#code-reviews)
    *   [Community guidelines](#community-guidelines)
*   [When to contribute](#when-to-contribute)
*   [Contributor workflow](#contributor-workflow)
*   [Overview of GDM architecture](#overview-of-gdm-architecture)
    *   [Manager](#manager)
    *   [Base classes](#base-classes)
    *   [Primary device classes](#primary-device-classes)
    *   [Auxiliary devices](#auxiliary-devices)
    *   [Capabilities](#capabilities)
    *   [Device communication architecture (Switchboard)](#device-communication-architecture-switchboard)
    *   [Device health checks](#device-health-checks)
*   [How to extend GDM](#how-to-extend-gdm)
    *   [Adding a new device class](#adding-a-new-device-class)
        *   [Primary device](#primary-device)
        *   [Auxiliary device](#auxiliary-device)
    *   [Adding a new communication type](#adding-a-new-communication-type)
    *   [Adding a new transport type](#adding-a-new-transport-type)
    *   [Adding a new detection query](#adding-a-new-detection-query)
    *   [Adding a new key](#adding-a-new-key)
    *   [Adding a new capability](#adding-a-new-capability)
*   [Other questions](#other-questions)

## General information

### Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License
Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
part of the project. Head over to <https://cla.developers.google.com/> to see
your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one
(even if it was for a different project), you probably don't need to do it
again.

### Code reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

### Community guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google/conduct/).

## When to contribute

GDM can be extended by extension packages. Extension package source code can
reside anywhere (i. e., internal company repositories) and does not have to be
checked into the upstream gazoo-device repository.

When not to contribute to gazoo-device Github repository:

*   You want to add a controller for a proprietary device and do not want to
    open-source the code. This can be accomplished by creating an extension
    package. The source code can be stored in your company's private repository.
    Refer to the
    [example extension package](https://github.com/google/gazoo-device/tree/master/examples/example_extension_package).

When to contribute to gazoo-device Github repository:

*   You are adding an open-source device controller. For instance, it could be
    an example application running on a new development board.
*   You are adding a proprietary device controller but need to extend or adjust
    the general GDM architecture to suit your case. The GDM architecture change
    may need to be checked in into the Github repo.
    *   Note that extension packages can define new communication types and
        detection criteria, so in most cases you should not need to check any
        code into the GDM Github repo.

## Contributor workflow

We are happy to accept contributions and guide you through the process. \
The contributor workflow has not been fully ironed out yet, so make sure to
start by sending an email to gdm-authors@google.com with an outline of your
planned change. We will review your proposal and advise on the next steps you
will need to take.

1.  [Sign a Contributor License Agreement](https://cla.developers.google.com/)
    if you haven't done so already. This only needs to be done once.
2.  [Open a new issue or use an existing one](https://github.com/google/gazoo-device/issues)
    to provide context on the bug or feature request. Include a description of
    the proposed implementation. We will review it and provide suggestions.
3.  After your proposed implementation idea is reviewed, proceed to writing code
    and tests.
4.  Your change must have incremental unit test coverage of >= 90% and pass all
    unit tests.

    Refer to the
    [unit test documentation](gazoo_device/tests/unit_tests/README.md).

5.  Your change must pass GDM on-device regression tests.

    Refer to the
    [functional test documentation](gazoo_device/tests/functional_tests/README.md).

6.  If existing functional tests do not cover your change, either add a new
    functional test or provide proof that the new features work on a real
    device. You can provide a snippet of a CLI or a Python interpreter
    interaction as proof.

7.  Open a Github pull request and add [artorl](https://github.com/artorl) as a
    reviewer.

## Overview of GDM architecture

### Manager

The `Manager` class ([gazoo_device/manager.py](gazoo_device/manager.py)) is
responsible for managing known devices and their configuration files. It also
keeps track of open device instances. `FireManager`, a subclass of `Manager`,
extends Manager functionality with methods that are intended to only be used
interactively from the GDM CLI. `FireManager` serves as the entry point for
GDM's CLI.

### Base classes

Devices commonly share a platform, which means that interactions with many smart
devices are similar. Such platform-specific features typically go into base
classes. For example, a base class for all smart devices running on Linux could
be `LinuxDevice`. Features which go into the base class are often tied to the
communication type or to a platform-specific binary. Base classes can be found
in [gazoo_device/base_classes/](gazoo_device/base_classes/).

Primary device base classes inherit from
[gazoo_device/base_classes/gazoo_device_base.py](gazoo_device/base_classes/gazoo_device_base.py).
\
Auxiliary device base classes inherit from
[gazoo_device/base_classes/auxiliary_device.py](gazoo_device/base_classes/auxiliary_device.py).

Base classes typically remain abstract.

### Primary device classes

A primary device class is a controller for a device under test. Primary device
classes must implement all methods and properties defined by
[gazoo_device/base_classes/primary_device_base.py](gazoo_device/base_classes/primary_device_base.py)
and must directly or indirectly inherit from
[gazoo_device/base_classes/gazoo_device_base.py](gazoo_device/base_classes/gazoo_device_base.py).
Typically:

*   There is a one-to-one mapping between physical devices and corresponding
    device classes.
*   Device classes extend the base class with device-specific functionality
    rather than directly inheriting from
    [gazoo_device/base_classes/gazoo_device_base.py](gazoo_device/base_classes/gazoo_device_base.py).

### Auxiliary devices

An auxiliary device class is a controller for a supporting device. Examples
include programmable USB hubs, power delivery units, and Ethernet switches.
Auxiliary device classes must implement all methods and properties defined by
[gazoo_device/base_classes/auxiliary_device_base.py](gazoo_device/base_classes/auxiliary_device_base.py)
and must directly or indirectly inherit from
[gazoo_device/base_classes/auxiliary_device.py](gazoo_device/base_classes/auxiliary_device.py).

Auxiliary devices are typically used indirectly through methods or capabilities
of primary devices. For example,
[`device_power`](gazoo_device/capabilities/device_power_default.py) capability
corresponds to the ability of Cambrionix (a programmable USB hub) to control
device power for USB-powered devices.

### Capabilities

Any additional features beyond the basics required by `PrimaryDeviceBase` or
`AuxiliaryDeviceBase` must be implemented as capabilities. Whereas the device
classes and base classes follow an inheritance model, capabilities are based on
composition. Device classes can mix and match different capability flavors
(implementations).

All capabilities inherit from the `CapabilityBase` interface defined in
[gazoo_device/capabilities/interfaces/capability_base.py](gazoo_device/capabilities/interfaces/capability_base.py).

A capability consists of the following:

*   An abstract interface in
    [gazoo_device/capabilities/interfaces/](gazoo_device/capabilities/interfaces/).
*   One or more flavors of the capability in
    [gazoo_device/capabilities/](gazoo_device/capabilities/). All flavors of a
    capability must implement the abstract interface. Ideally, API signatures of
    different capability flavors remain identical despite the underlying
    implementation differences.
*   A capability definition in a base or device class. The definition adds the
    capability to the device or base class and supplies it with the necessary
    initialization arguments.

### Device communication architecture (Switchboard)

Switchboard is the multiprocessing architecture behind GDM's device
communication. It handles device communication, logging, and event filtering.
Switchboard serves as an abstraction layer on top of different communication
types such as SSH, ADB, RPC, or UART. The
[`SwitchboardDefault` class](gazoo_device/switchboard/switchboard.py) exposes
several high-level device communication methods, such as `send_and_expect()` and
`expect()`. Base and device classes use Switchboard to communicate with physical
devices.

Switchboard uses several child processes to accomplish its goals. It uses one or
more `TransportProcess`es, a `LogFilterProcess`, and a `LogWriterProcess`.

*   Each `TransportProcess` manages a single device transport, which is a
    bidirectional communication channel with the device (such as an `ssh`
    subprocess).
    *   [Communication types](gazoo_device/switchboard/communication_types.py)
        define which transports should be used.
*   `LogWriterProcess` records all device communications to a device log file.
*   `LogFilterProcess` looks for specific event markers in the logs and records
    them to a separate event file.

### Device health checks

Health check execution can be triggered through 3 different ways:

1.  During device detection.
2.  During device creation (optional: `make_device_ready` can be set to `off`).
3.  On-demand via `<device>.make_device_ready()` or through `FireManager`
    `make_devices_ready` and `health_check` methods.

There are 4 modes (settings) in which health checks (`make_device_ready`) can
run:

1.  `"off"`: `make_device_ready` returns immediately without checking anything.
2.  `"check_only"`: health checks will run once. The first encountered error
    will be reraised, and recovery will not be attempted;
3.  `"on"`: health checks will run. If an error is encountered, recovery (if
    available) will be attempted. Health checks will run again after recovery to
    verify that recovery succeeded. The health check -> recovery -> health check
    loop can be performed several times. If an unrecoverable error is
    encountered or recovery runs out of attempts, the error is reraised.
4.  `"flash_build"`: same as `"on"`, but if an uncoverable error is encountered
    and the device has a `flash_build` capability, attempt to reflash the device
    as a last-resort recovery instead of reraising the error.

## How to extend GDM

GDM is designed to be extensible with extension packages. Extension packages can
define:

*   primary, auxiliary, and virtual device classes (controllers);
    *   log event filters for the new controllers;
*   capability interfaces and capability flavors (implementations);
*   communication types;
    *   including new communication transports;
*   detection criteria for each communication type;
    *   including new detection queries;
*   metadata (extension package name and version);
*   keys (such as SSH or API keys).

In addition to the above, extension packages must define:

*   a key download function (`download_key`);
*   a package version (`__version__`).

Extension packages make functionality defined within them available to GDM by
exporting it via a `export_extensions` function.
[gazoo_device/package_registrar.py](gazoo_device/package_registrar.py) documents
the expected return format of `export_extensions`. \
GDM's open-source device controllers are implemented as a built-in extension
package
([gazoo_device/gazoo_device_controllers.py](gazoo_device/gazoo_device_controllers.py)).

To register an extension package with GDM from Python, call

```python
gazoo_device.register(<your-extension-package-init-module>)
```

Python package registration **is not** persistent. Registered packages are
"forgotten" when Python interpreter shuts down. Packages need to be registered
at each test run (or each new interpreter session).

To register a package for use with GDM CLI:

```shell
<virtual_env_path>/bin/pip install my_extension_package
<virtual_env_path>/bin/gdm register my_extension_package
```

To unregister a package from GDM CLI:

```shell
<virtual_env_path>/bin/gdm unregister my_extension_package
```

CLI package registration **is** persistent. CLI packages are not available for
use from a Python environment.

For a hands-on introduction to extension packages, try the
[extension package codelab](https://github.com/google/gazoo-device/blob/master/examples/example_extension_package/README.md).

### Adding a new device class

#### Primary device

Primary device classes implement all methods of the
[`PrimaryDeviceBase` interface](gazoo_device/base_classes/primary_device_base.py).
The typical pattern is to create a base class corresponding to a common device
platform and then create one or more device classes inheriting from the base
class. However, creating a base class is not required, and all device
functionality can reside directly in the device class. The new base class (or
the device class) must directly or indirectly inherit from
[`GazooDeviceBase`](gazoo_device/base_classes/gazoo_device_base.py).

A device class typically has the following:

*   A logger instance:

    ```python
    logger = gdm_logger.get_logger()
    ```

*   Commands, regular expressions, and timeouts:

    *   A `COMMANDS` dictionary, where the key is a human-readable command
        description (`"FIRMWARE_VERSION"`), and the value is the command to
        retrieve it.

    *   A `REGEXES` dictionary, where the key is a human-readable description
        typically matching the COMMANDS entry (`"FIRMWARE_VERSION"`), and the
        value is the regex to retrieve the desired value from the command
        response (`r"(\d.\d+)"`).

    *   A `TIMEOUTS` dictionary, where the key is the name of the operation, and
        the value is the timeout in seconds (`{"REBOOT": 30}`).

*   Communication type information:

    *   A `COMMUNICATION_TYPE` class constant, which is a string specifying
        which communication type should be used (`COMMUNICATION_TYPE =
        "SshComms"`). All built-in communication types can be found in
        [gazoo_device/switchboard/communication_types.py](gazoo_device/switchboard/communication_types.py).

    *   A `_COMMUNICATION_KWARGS` class dictionary, which contains all
        communication arguments other than the communication address
        (`comms_address`). For example, for `"SshComms"`:

        ```python
        _COMMUNICATION_KWARGS = {
            "ssh_key_type": None,
            "username": "root",
        }
        ```

        Each communication type has unique arguments. Refer to `__init__`
        methods of `CommunicationType` classes to see the supported arguments
        and their purpose.

*   Log event filters:

    *   One or more JSON log event filters. See the
        [example device controller log event filters](examples/example_extension_package/log_event_filters/)
        to understand the expected JSON format.

    *   A `_DEFAULT_FILTERS` class constant, which is a list of strings
        specifying absolute paths to log event filters for the device:

        ```python
        _DEFAULT_FILTERS = [
            os.path.join("some_log_event_filter_directory/", "basic.json"),
            os.path.join("some_log_event_filter_directory/", "crashes.json"),
        ]
        ```

    *   At a minimum, each device has a *basic.json* filter, which declares
        "bootup" and "reboot_trigger" events. The "bootup" event should match a
        log line emitted by the device only once during each boot up. The
        "reboot_trigger" events are logged by GDM itself. A typical reboot
        implementation will log a certain message and then issue a device
        command to reboot. Make sure that the log line emitted by the device
        class during reboot matches the event filter (`"GDM triggered reboot"`
        is typically used).

    *   Additional events, such as crashes or state changes, can be appended to
        the *basic.json* filter or go into a separate filter file.

    *   The event name used by GDM is a combination of the filter file name and
        the event name (`"basic.bootup"`, `"basic.reboot_trigger"`).

*   An `__init__` method, which updates `self.commands`, `self.regexes`, and
    `self.timeouts` with key-value pairs from `COMMANDS`, `REGEXES`, and
    `TIMEOUTS` dictionaries.

*   An `is_connected` class method, which determines whether the device is
    connected to the host. The method is given the full Manager device config
    (`device_config`). The typical implementation checks whether the main
    communication port (`device_config["persistent"]["console_port_name"]`) is
    visible to the host, which may be pinging the IP address or checking if the
    serial path exists.

*   Health checks and corresponding recovery mechanisms:

    *   One or more health check methods. Health check method naming convention
        is `check_<action>`, such as `check_device_responsiveness`.

    *   Health check methods check that the device is ready for use. Typical use
        cases are checking device responsiveness and ensuring the testbed is set
        up correctly. If the device is not ready, an error specifying the issue
        should be raised. Errors raised by health checks must be subclasses of
        `CheckDeviceReadyError`. See
        [gazoo_device/errors.py](gazoo_device/errors.py) for a full list of
        possible errors. While most of the common errors already exist, you
        might want to define a new error type if you have a more specific health
        check.

    *   A `health_checks` persistent property must return a list of all health
        check methods to run. Health checks will run in this order. Note that
        `GazooDeviceBase` defines two health check methods which are typically
        run first by all devices. The typical return value of `health_checks` is
        `[self.check_device_connected, self.check_create_switchboard,
        <additional health checks>]`.

    *   Caveat: be careful with accessing persistent properties and capabilities
        which use them in health checks. There is nothing special about running
        health checks during device creation or on-demand later, but running
        them during device detection presents a corner case. When health checks
        run during detection, persistent properties have not been populated by
        `get_detection_info` yet. If you must use a persistent property during a
        health check, consider making a getter function for it and using the
        getter during the health check. The function can then be used to
        populate the persistent property in `get_detection_info`. Alternatively,
        if the health check depends on persistent properties and is not
        essential, it can be skipped during the detection process by checking
        the value of `self.is_detected()`, which is `False` during the detection
        process.

    *   A `recover` method, which accepts an error raised by a health check (a
        subclass of `CheckDeviceReadyError`) and runs an appropriate recovery
        mechanism. If there is no recovery mechanism for the given error, it
        should be reraised (`raise error`). Note that the most common recovery
        mechanism is rebooting or power cycling the device.

    *   The maximum number of recovery attempts is defined by
        `_RECOVERY_ATTEMPTS` class constant (defaults to 1).

*   A `shell` method, which executes a given shell command on the device. The
    typical implementation sends the command to the device and expects a regular
    expression (response and optionally a return code) back. `shell()` is
    typically implemented by calling `self.switchboard.send_and_expect`. Note
    that in some cases there may not be a `shell` method (if the device does not
    support shell command execution), but the vast majority of devices should
    implement it.

    *   Most other device methods and capabilities should use `shell()` to
        control the device instead of calling `send_and_expect()` directly.

*   A `get_detection_info` method, which queries the device for all persistent
    properties (`self.props["persistent_identifiers"]`) during detection.
    Optional properties (`self.props["options"]`) should be initialized to an
    appropriate value (typically `None`) here as well. The method should return
    a tuple of `self.props["persistent_identifiers"], self.props["options"]`.

    *   You do not need to worry about storing the values in a file. GDM
        automatically stores persistent and optional device configs to files
        (`~/gazoo/gdm/conf/devices.json` and
        `~/gazoo/gdm/conf/device_options.json`).
    *   The communication address of the device will already be populated by
        GDM. It is available as `self.communication_address`.
    *   There are two persistent properties that **must** be populated: "model"
        and "serial_number".
        *   "model" refers to the hardware model of the device (such as
            prototype, development, or production).
        *   "serial_number" is typically the device's serial number, but can be
            any persistent unique identifier. The 4 last characters of this
            property are used to create the device name, which has the format
            `devicetype-1234`.

*   Implementations of other abstract methods (such as `reboot`,
    `wait_for_bootup_complete`). These methods should use the `shell` method to
    communicate with the device where possible.

    *   All public device methods which do not return a value must be decorated
        with `@decorators.LogDecorator(logger)`. The log decorator will log
        messages when a method begins and finishes executing (including how long
        the method took), as well as specially-formatted messages for errors.

*   Additional properties. There are 3 types of properties: persistent, dynamic,
    and optional. Use the appropriate decorator to define each property type
    (`@decorators.PersistentProperty`, `@decorators.DynamicProperty`, or
    `@decorators.OptionalProperty`). The decorators can be found in
    [gazoo_device/decorators.py](gazoo_device/decorators.py).

    *   Persistent properties are constant for a physical device. A good example
        is the device's serial number. These properties are retrieved during
        detection (`gdm detect`) and stored in a config file.
    *   Dynamic properties can change at any time. The values of these
        properties are not cached. Instead, they are always retrieved at access
        time. An example of a dynamic property is "firmware_version".
    *   Optional properties are properties which can be set by the user, but are
        not required by GDM. Some examples include accounts, passwords, or names
        and ports of optional supporting devices (such as a USB hub).

*   Additional capability definitions.

    *   Any device functionality beyond the basics required by
        `PrimaryDeviceBase` or `AuxiliaryDeviceBase` must be implemented as
        capabilities.
    *   Each capability must be denoted by
        `@decorators.CapabilityDecorator(<capability class>)`. Note that the
        name of the capability definition must match the expected name for the
        capability. The expected name is generated from the interface by
        removing the "Base" suffix and converting the `PascalCase` interface
        name into `snake_case` capability name. For example: `FileTransferBase`
        -> `file_transfer`.
    *   The capability definition should return
        `self.lazy_init(<capability_class>, arg1=value1, arg2=value2)`.
        `GazooDeviceBase.lazy_init` provides a lazy initialization mechanism for
        capabilities. Pass all capability `__init__` arguments via keywords for
        readability.
    *   Capability definitions allow base and device classes to customize
        capabilities by providing capability initialization arguments. For
        example, it is possible to pass some device-specific values (like a
        `self.commands` dictionary) during initialization.
    *   To reset (re-initialize) a capability, issue
        `self.reset_capability(<capability_class>)` and access the capability
        again.
    *   Full example of a capability definition:

    ```python
    @decorators.CapabilityDecorator(file_transfer_scp.FileTransferScp)
    def file_transfer(self):
      """File transfer capability for moving files from and to the device."""
      return self.lazy_init(
          file_transfer_scp.FileTransferScp,
          ip_address_or_fn=self.ip_address,
          device_name=self.name,
          add_log_note_fn=self.switchboard.add_log_note,
          user=self._COMMUNICATION_KWARGS["username"],
          key_info=self._COMMUNICATION_KWARGS["key_info"])
    ```

#### Auxiliary device

Auxiliary devices are very similar to primary devices, but the requirements are
less stringent. Auxiliary devices have their own interface
([`AuxiliaryDeviceBase`](gazoo_device/base_classes/auxiliary_device_base.py))
and base class
([`AuxiliaryDevice`](gazoo_device/base_classes/auxiliary_device.py)). Auxiliary
devices must inherit from `AuxiliaryDevice`.

Differences between primary and auxiliary devices:

* auxiliary devices are not required to have a Switchboard and define a
  communication type;
* auxiliary devices do not support log event filters;
* auxiliary devices are not required to implemented the following methods and
  properties: `wait_for_bootup_complete`, `firmware_version`, `os`, `platform`,
  `reboot`, `factory_reset`, `shell`.

Auxiliary devices are identical to primary devices in all other aspects.

### Adding a new communication type

A communication type identifies communication addresses that belong to it and
defines transports, line identifiers, and transport initialization arguments
that should be used for the given communication address. Some (included)
communication type examples are `SerialComms` and `SshComms`.Communication types
are defined in
[gazoo_device/switchboard/communication_types.py](gazoo_device/switchboard/communication_types.py)
and derive from the `CommunicationType` abstract base class (ABC).

Communication types must implement the following methods:

*   `get_comms_addresses()`: returns a list of all communication addresses (such
    as IP addresses or serial paths) on the host which can be used by a device
    using this communication address. For example, for serial devices, this
    typically means listing USB entries under /dev. IP addresses are provided as
    an argument to detection (`--static_ips`).
*   `get_transport_list()`: returns a list of initialized transports to be used
    by the communication type.
*   `get_identifier()`: returns a line identifier, which tells GDM whether an
    incoming device communication line is a log, a device response, or should
    get classified as "unknown". Line identifiers can be found in
    [gazoo_device/switchboard/line_identifier.py](gazoo_device/switchboard/line_identifier.py).

Each device class defines what communication type it uses in the
`COMMUNICATION_TYPE` class constant (such as `COMMUNICATION_TYPE = "SshComms"`).
Any additional keyword arguments pertinent to the communication setup besides
the main communication address are placed in the `_COMMUNICATION_KWARGS`
dictionary of the device class. The main device communication address gets
populated by GDM automatically after detection.

Each communication type defines new or reuses existing detection queries in
[gazoo_device/detect_criteria.py](gazoo_device/detect_criteria.py). For example,
for serial devices, one of the queries retrieves the USB product name. For SSH
devices, there are several queries, each of which runs a certain shell command
on the device.

During the detection process, GDM:

1.  identifies all potential connections by calling `get_comms_addresses()` of
    all supported communication types;
2.  filters out connections corresponding to already known devices;
3.  runs all detection queries and records their responses for each potential
    connection;
4.  identifies all device classes which could use this communication type by
    checking their communication type (`<device_class>.COMMUNICATION_TYPE`);
5.  asks each applicable device class whether the connection should be
    associated with the device class by checking whether the recorded detection
    query responses satisfy the detection match criteria specified by the device
    class (`<device_class>.DETECT_MATCH_CRITERIA`).

### Adding a new transport type

A transport is a bidirectional communication channel with the device. Most GDM
device communications go through transports. The only significant exception to
this is HTTP requests, which are performed by
[gazoo_device/utility/http_utils.py](gazoo_device/utility/http_utils.py).

Transports can be found in
[gazoo_device/switchboard/transports](gazoo_device/switchboard/transports/).
Each transport implements a transport interface defined in
[gazoo_device/switchboard/transports/transport_base.py](gazoo_device/switchboard/transports/transport_base.py).
The transport interface defines methods for closing, opening, reading from, and
writing to the transport.

Transports are managed by `TransportProcess`es
([gazoo_device/switchboard/transport_process.py](gazoo_device/switchboard/transport_process.py)),
which are child processes. The main process does not interact with transports
directly. Instead, it sends commands to the child processes.

### Adding a new detection query

Detection queries are comprised of a query key and of a corresponding query
function.

*   Query keys are defined as enums: subclasses of `detect_criteria.QueryEnum`
    ([gazoo_device/detect_criteria.py](gazoo_device/detect_criteria.py)). When
    adding a new key, either define a new `QueryEnum` subclass and add your key
    to it or add the new key to an existing subclass. Because detection criteria
    are grouped by communication types, `QueryEnum` subclasses are named after
    communication types.
*   Query functions all have the same signature. They accept 3 arguments:
    communication address, logger, and Switchboard creation callable. The
    query's goal is to collect some information from the communication address.
    Query logs (i. e., match, no match, or errors) should be logged via the
    provided logger. If the query needs to perform some non-trivial
    communication, it is recommended to create a Switchboard instance for
    communication with the device (make sure to close the Switchboard instance
    when you are done). The query can return `True`, `False`, or a string. If a
    string is returned, device classes can perform regex matching on the
    returned response. An example of a True/False query: checking whether the
    device has a certain binary. An example of a string/regex query: device USB
    product name.
*   Query keys are mapped to the corresponding query functions via dictionaries.

Device classes use detection queries by defining a `DETECT_MATCH_CRITERIA`
dictionary, which maps the available detection query keys to expected values or
regexes. If all detection criteria defined by a device class match the
connection, the connection is recognized as belonging to this device class.
Here's an example of detection criteria for Raspberry Pi:

```python
class RaspberryPi(raspbian_device.RaspbianDevice):
  DETECT_MATCH_CRITERIA = {
      detect_criteria.SshQuery.is_rpi: True,
  }
```

Since detection queries are tied to the communication type, the set of available
queries is defined by `COMMUNICATION_TYPE` of the device class:

```python
class RaspbianDevice(auxiliary_device.AuxiliaryDevice):
  COMMUNICATION_TYPE = "SshComms"
```

### Adding a new key

Extension packages may need to use SSH or API keys. GDM has a mechanism which
allows extension packages to register key information and a hook to download the
matching key. Keys are downloaded on an as-needed basis. However, you can force
GDM to download all registered keys by running `gdm download-keys`.

*   Key information is defined as `data_types.KeyInfo` instances (see
    [gazoo_device/config.py](gazoo_device/config.py) for an example).
*   The key download hook is a `download_key` function defined by the extension
    package. It accepts a `KeyInfo` instance and the expected local path of the
    key. The function needs to obtain the key and save it in a file with the
    given local path. `download_key` is only called if the key does not exist
    yet. The local folder where the key is expected to be stored is guaranteed
    to exist.

### Adding a new capability

Any public functionality beyond the basics required by the primary or auxiliary
device interfaces must be placed in capabilities.

Each capability consists of 3 parts:

1.  Capability interface. These are found in
    [gazoo_device/capabilities/interfaces](gazoo_device/capabilities/interfaces).
    The capability interface defines a device-agnostic contract which all
    implementations adhere to. Each interface must inherit from the
    [`CapabilityBase` class](gazoo_device/capabilities/interfaces/capability_base.py)
    and is typically abstract. Note that the capability name is derived from the
    interface class name. For example: `FileTransferBase` -> `file_transfer`.
2.  One or more capability flavors (implementations). Each must inherit from the
    relevant capability interface. For example, `FileTransferBase` interface is
    implemented by `FileTransferScp` and `FileTransferAdb`.

    *   All public capability methods which do not return a value must be
        decorated with `@decorators.CapabilityLogDecorator(logger)`. The log
        decorator will log messages when a method begins and finishes executing
        (including how long the method took), as well as specially-formatted
        messages for errors.

3.  Device capability definitions. Capability definitions are used to add
    capabilities to base or device classes. Note that the capability name must
    match the name derived from the interface. For example, a class using
    `FileTransferAdb` must define the capability as `def file_transfer(self):`.
    Use the capability decorator (`CapabilityDecorator` in
    [gazoo_device/decorators.py](gazoo_device/decorators.py)) to denote
    capability definitions. Use `GazooDeviceBase.lazy_init` to initialize the
    capability.

## Other questions

Still have questions?

Try looking at the
[example device extension package](https://github.com/google/gazoo-device/tree/master/examples/example_extension_package)
and the existing
[base & device classes, communication types, transports, and capabilities](https://github.com/google/gazoo-device/tree/master/gazoo_device).
\
If that fails, open a
[new Githib issue](https://github.com/google/gazoo-device/issues/new) with your
question or send us an email at gdm-authors@google.com.
