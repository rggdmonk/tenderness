# Copyright 2026 Pavel Stepachev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Fontconfig XML templates."""

from __future__ import annotations

from string import Template

# --------------------------
# DARWIN (MacOS)
# --------------------------
DARWIN_FONTCONFIG_TEMPLATE_CONFIG_MINIMAL = Template("""<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
    <dir>$font_dir</dir>
</fontconfig>
""")

DARWIN_FONTCONFIG_TEMPLATE_INSERT_FONT_DIR = Template("\t<dir>$font_dir</dir>\n")
DARWIN_FONTCONFIG_REMOVE_SYSTEM_FONTS_PATTERNS = ("/System/Library/", "/Library", "~/Library", "~/.fonts")


# --------------------------
# LINUX
# --------------------------
LINUX_FONTCONFIG_TEMPLATE_CONFIG_MINIMAL = Template("""<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
    <dir>$font_dir</dir>
</fontconfig>
""")

LINUX_FONTCONFIG_TEMPLATE_INSERT_FONT_DIR = Template("\t<dir>$font_dir</dir>\n")
LINUX_FONTCONFIG_REMOVE_SYSTEM_FONTS_PATTERNS = ("/usr/share/fonts", "/usr/local/share/fonts", "~/.fonts")
