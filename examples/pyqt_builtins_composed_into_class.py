#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import sys

from pytraits import add_traits, setproperty

try:
    from PyQt5.QtWidgets import QSpinBox, QApplication, QLineEdit

    # We need an application to get things done.
    app = QApplication(sys.argv)

    # Define a controller that encapsulates handling of two UI components that
    # are closely linked together.
    class UiController:
        pass

    # Create two UI widgets
    spinner = QSpinBox()
    line_edit = QLineEdit()

    # Update controller by adding functions and property from builtin components.
    add_traits(UiController, line_edit.text, line_edit.setText)
    setproperty(UiController, spinner.value, spinner.setValue, name="answer")

    # Create controller
    ctrl = UiController()
    ctrl.answer = 42
    ctrl.setText("Life, Universe...")

    # And here's the proof that properties and functions are working and they
    # modify correct widgets.
    assert ctrl.answer == 42, "Spinner property is unaware of the answer!"
    assert ctrl.text() == "Life, Universe...", "Text property is unaware of nature of the answer!"
    assert ctrl.answer == spinner.value(), "UiController and QSpinBox widget are not communicating!"
    assert ctrl.text() == line_edit.text(), "UiController and QLineEdit widget are not communicating!"
except ImportError:
    pass  # Skipping since PyQt is not available
