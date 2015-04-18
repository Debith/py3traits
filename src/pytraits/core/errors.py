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
BuiltinSourceError = 'Built-in objects can not used as traits!'
PropertySourceError = 'Properties can not be extended!'


# Convert strings to exception objects
for exception, message in dict(globals()).items():
    if not exception.endswith('Error'):
        continue
    bases = (Exception,)
    attrs = {'_MSG': message,
             '__str__': lambda self: self._MSG}
    globals()[exception] = type(exception, bases, attrs)
