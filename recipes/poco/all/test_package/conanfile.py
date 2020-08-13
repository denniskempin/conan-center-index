import os
from conans import CMake, ConanFile, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    @property
    def _with_encodings(self):
        return "enable_encodings" in self.options["pocos"] and self.options["poco"].enable_encodings == True

    @property
    def _with_jwt(self):
        return "enable_jwt" in self.options["poco"] and self.options["poco"].enable_jwt == True

    def build(self):
        cmake = CMake(self)
        cmake.definitions["TEST_CRYPTO"] = self.options["poco"].enable_crypto == True
        cmake.definitions["TEST_UTIL"] = self.options["poco"].enable_util == True
        cmake.definitions["TEST_NET"] = self.options["poco"].enable_net == True
        cmake.definitions["TEST_NETSSL"] = self.options["poco"].enable_netssl == True
        cmake.definitions["TEST_SQLITE"] = self.options["poco"].enable_data_sqlite == True
        cmake.definitions["TEST_ENCODINGS"] = self._with_encodings
        cmake.definitions["TEST_JWT"] = self._with_jwt
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings, skip_x64_x86=True):
            self.run(os.path.join("bin", "core"), run_environment=True)
            if self.options["poco"].enable_util:
                self.run(os.path.join("bin", "util"), run_environment=True)
            if self.options["poco"].enable_crypto:
                self.run("{} {}".format(os.path.join("bin", "crypto"), os.path.join(self.source_folder, "conanfile.py")), run_environment=True)
            if self.options["poco"].enable_net:
                self.run(os.path.join("bin", "net"), run_environment=True)
                self.run(os.path.join("bin", "net_2"), run_environment=True)
            if self.options["poco"].enable_netssl:
                self.run(os.path.join("bin", "netssl"), run_environment=True)
            if self.options["poco"].enable_data_sqlite:
                self.run(os.path.join("bin", "sqlite"), run_environment=True)
            if self._with_encodings:
                self.run(os.path.join("bin", "encodings"), run_environment=True)
            if self._with_jwt:
                self.run(os.path.join("bin", "jwt"), run_environment=True)
