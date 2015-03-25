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

# Exceptions
UnextendableObjectError = "Target context can be only class or instance of class"
InvalidAssignmentError = "Not possible to assign a key"
SingletonError = 'Singletons are immutable'

# Convert the strings to actual exception:
#  - Variable name is converted to type of exception.
#  - Variable value is added as message.
from .magic import create_exception_classes
exec(create_exception_classes)
