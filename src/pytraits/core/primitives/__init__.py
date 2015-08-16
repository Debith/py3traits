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

import pkgutil
import importlib
from os.path import dirname
from pytraits.support import is_sysname
from ..base.inspectors import TraitSourceInspector, TraitTargetInspector

# Import each module and register their TraitObject based classes to
# corresponsing inspectors. This mechanism allows us to add new modules and
# classes without need to do any other steps to get them registered into
# inspectors.
for _, module_name, _ in pkgutil.iter_modules([dirname(__file__)]):
    module = importlib.import_module("{}.{}".format(__package__, module_name))

    for object_name in dir(module):
        if is_sysname(object_name):
            continue

        object = getattr(module, object_name)

        try:
            object.hook_into(TraitSourceInspector)
            object.hook_into(TraitTargetInspector)
        except AttributeError:
            pass

# Let's remove the option of modifying the singletons after we are done with
# this.
TraitTargetInspector.add_hook = None
TraitTargetInspector.add_default_hook = None
TraitSourceInspector.add_hook = None
TraitSourceInspector.add_default_hook = None
