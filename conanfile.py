#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class CppTOMLConan(ConanFile):
    name = "cpptoml"
    version = "master"  # Last version is v0.4.0 from Feb 2015 (asking for new revision: https://github.com/skystrife/cpptoml/issues/42)
    url = "https://github.com/bincrafters/conan-cpptoml"
    description = "cpptoml is a header-only library for parsing TOML "

    # Indicates License type of the packaged library
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"build_examples": [True, False]}
    default_options = ("build_examples=False", )

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        source_url = "https://github.com/skystrife/cpptoml"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        
        tools.replace_in_file("{0}/CMakeLists.txt".format(extracted_dir),
            "list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/deps/meta-cmake)",
            "")

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CPPTOML_BUILD_EXAMPLES"] = self.options.build_examples
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
    
    def package_id(self):
        self.info.header_only()

