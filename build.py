#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init
import os
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.integrationtest")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.django")


name = "django-todolist"
default_task = "publish"

@init
def initialize():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

@init
def set_properties(project):
    project.set_property("dir_source_main_python", "src/main")
    project.set_property("dir_source_unittest_python", "src/unittest")
    project.set_property("coverage_break_build", False) 
    #settings.configure()
    # project.set_property("unittest_test_method_prefix" , "test_")
    project.set_property("unittest_module_glob","test_")