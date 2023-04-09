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

from pytraits.support import Singleton, Factory, type_safe, type_converted
from pytraits.combiner import combine_class
from pytraits.extendable import extendable
from pytraits.setproperty import setproperty
from pytraits.trait_composer import add_traits

__version__ = "1.2.1"
__all__ = ["Singleton", "Factory", "combine_class", "extendable", "add_traits",
           "type_safe", "type_converted", "setproperty"]
