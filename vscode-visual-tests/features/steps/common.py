"""Implementation of common test steps."""

# vim: set fileencoding=utf-8

#
#  (C) Copyright 2019  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

from behave import given, then, when
from time import sleep
from os import system, environ
from src.ps import get_process_list

VSCODE_COMMAND_NAME = "code"


@given('The PyAutoGUI library is initialized')
def initialize_autogui_library(context):
    """Initialize PyAutoGUI library and check display etc."""
    import pyautogui
    # must not be None
    assert pyautogui is not None
    # pause time (in seconds) for GUI operations
    pyautogui.PAUSE = 1.0
    context.pyautogui = pyautogui


@given('The screen resolution is at least {width:d}x{height:d} pixels')
def check_screen_size(context, width, height):
    """Check the screen size, because the UI layout depends on it."""
    assert context is not None
    actual_width, actual_height = context.pyautogui.size()

    assert actual_width >= width, "Insuficient screen width {w}".format(w=actual_width)
    assert actual_height >= height, "Insuficient screen height {h}".format(h=actual_height)


@given('The Visual Studio Code is set up')
def check_visual_studio_code_version(context):
    """Check whether the VS_CODE_VERSION environment variable is set."""
    env = environ
    assert env is not None
    assert "VS_CODE_VERSION" in env
    context.vs_code_version = env["VS_CODE_VERSION"]


@when('I start the Visual Studio Code')
def start_visual_studion_code(context):
    """Start the Visual Studio Code."""
    system(VSCODE_COMMAND_NAME)
    # time to breath
    sleep(2)


@when('I wait {num:d} seconds')
@then('I wait {num:d} seconds')
def pause_scenario_execution(context, num):
    """Pause the test for provided number of seconds."""
    sleep(num)


@then('I should find Visual Studio Code instance')
def visual_studio_code_instance(context):
    """Check that the Visual Studio Code has been started."""
    ps_output = get_process_list()

    for line in ps_output:
        if line.startswith("/usr/share/code"):
            # ok, we have probably found a running instance of Visual Studio Code
            return

    raise Exception("Visual Studio Code is not running")


@then('I should not find any Visual Studio Code instance')
def no_visual_studio_code_instance(context):
    """Check that the Visual Studio Code has not been started."""
    ps_output = get_process_list()

    for line in ps_output:
        if line.startswith("/usr/share/code"):
            # we have probably found a running instance of Visual Studio Code
            raise Exception("Visual Studio Code is running")
