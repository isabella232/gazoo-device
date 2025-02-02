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

"""Device logs for unifi poe switch."""

RETURN_CODE = "0\n"
ERROR_RETURN_CODE = "127\n"

DEFAULT_BEHAVIOR = {
    "mca-cli-op info;echo Return Code: $?\n":
        f"""
        Model:       USW-8P-150
        Version:     4.3.13.11253
        MAC Address: e0:63:da:54:3d:2a
        IP Address:  123.45.67.89
        Hostname:    UBNT
        Uptime:      44625 seconds

        Status:      Unknown[11] (http://123.45.67.90:8080/inform)

        Return Code: {RETURN_CODE}""",
    "reboot;echo Return Code: $?\n":
        f"""
        Return Code: {RETURN_CODE}""",
    "sh -c 'echo \"--- GDM Log Marker ---\" >> /var/log/messages';echo Return "
    "Code: $?\n":
        f"""
        Return Code: {RETURN_CODE}""",
    "echo 'exit' | telnet localhost;echo Return Code: $?\n":
        f"""
        Return Code: {RETURN_CODE}\n""",
}

HEALTH_CHECK_FAILURE = {
    "echo 'exit' | telnet localhost;echo Return Code: $?\n":
        f"""
        Return Code: {ERROR_RETURN_CODE}\n""",
}

TELNET_COMMAND_RESPONSES = {
    "telnet localhost\n":
        """
        Entering character mode
        Escape character is '^]'.

        Warning!
        The changes may break controller settings and only be effective until reboot.

        (UBNT) >""",
    "enable\n":
        "(UBNT) #",
    "config\n":
        "(UBNT) (Config)#",
    "interface 0/1\n":
        "(Interface 0/1)#",
    "interface 0/2\n":
        "(Interface 0/2)#",
    "interface 0/3\n":
        "(Interface 0/3)#",
    "interface 0/4\n":
        "(Interface 0/4)#",
    "interface 0/5\n":
        "(Interface 0/5)#",
    "interface 0/6\n":
        "(Interface 0/6)#",
    "interface 0/7\n":
        "(Interface 0/7)#",
    "interface 0/8\n":
        "(Interface 0/8)#",
    "exit\n":
        """
        Connection closed by foreign host
        (UBNT) >
        (UBNT) #
        (UBNT) (Config)#
    """,
    "show hardware\n":
        """
        Switch: 1

        System Description............................. USW-8P-150, 4.3.13.11253, Linux 3.6.5
        Machine Type................................... USW-8P-150
        Machine Model.................................. US8P150
        Serial Number.................................. e063da543d2a
        Burned In MAC Address.......................... E0:63:DA:54:3D:2A
        Software Version............................... 4.3.13.11253

        (UBNT) #"""
}

SHOW_POE_PORT_AUTO = {
    "show poe port 0/1\n":
        """
        (UBNT) (Config)#show poe port 0/1

                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/1       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/2\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/2       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/3\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/3       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/4\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/4       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/5\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/5       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/6\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/6       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/7\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/7       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/8\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/8       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port all\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/1       Auto             Enable  802.3at Enable  Enable     Enable
        0/2       Auto             Enable  802.3at Enable  Enable     Enable
        0/3       Auto             Enable  802.3at Enable  Enable     Enable
        0/4       Auto             Enable  802.3at Enable  Enable     Enable
        0/5       Auto             Enable  802.3at Enable  Enable     Enable
        0/6       Auto             Enable  802.3at Enable  Enable     Enable
        0/7       Auto             Enable  802.3at Enable  Enable     Enable
        0/8       Auto             Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#"""
}

SHOW_POE_PORT_SHUTDOWN = {
    "show poe port 0/1\n":
        """
        (UBNT) (Config)#show poe port 0/1

                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/1       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/2\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/2       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/3\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/3       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/4\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/4       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/5\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/5       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/6\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/6       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/7\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/7       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port 0/8\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/8       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#""",
    "show poe port all\n":
        """
                OP               HP      HP      Detect  Disconnect Class
        Intf      Mode             Enable  Mode    Enable  Enable     Enable
        --------- ---------------- ------- ------- ------- ---------- -------
        0/1       Shutdown         Enable  802.3at Enable  Enable     Enable
        0/2       Shutdown         Enable  802.3at Enable  Enable     Enable
        0/3       Shutdown         Enable  802.3at Enable  Enable     Enable
        0/4       Shutdown         Enable  802.3at Enable  Enable     Enable
        0/5       Shutdown         Enable  802.3at Enable  Enable     Enable
        0/6       Shutdown         Enable  802.3at Enable  Enable     Enable
        0/7       Shutdown         Enable  802.3at Enable  Enable     Enable
        0/8       Shutdown         Enable  802.3at Enable  Enable     Enable


        (UBNT) (Config)#"""
}
