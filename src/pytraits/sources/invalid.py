#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
'''
   Copyright 2014-2015 Teppo Perä

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''


class InvalidSource(object):
    """
    Null context for invalid cases.
    """
    BINDER_ID = 'null'
    VALID = False

    def __init__(self, extra_message):
        print("PyTraits: InvalidContext:", extra_message)
        self._extra_message = extra_message

    @property
    def error_message(self):
        return self._extra_message
