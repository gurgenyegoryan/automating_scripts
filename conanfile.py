from conans import ConanFile, CMake, tools
import os

class RocksDBConan(ConanFile):
    name = "rocksdb"
    version = "7.10.2"
    license = "GPL-2.0-only"
    url = "https://github.com/facebook/rocksdb"
    description = "A library that provides an embeddable, persistent key-value store for fast storage."
    topics = ("conan", "rocksdb", "database", "key-value")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "lite": [True, False],
        "with_gflags": [True, False],
        "with_snappy": [True, False],
        "with_lz4": [True, False],
        "with_zlib": [True, False],
        "with_zstd": [True, False],
        "with_tbb": [True, False],
        "with_jemalloc": [True, False],
        "enable_sse": [False, "sse42", "avx2"],
        "use_rtti": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": False,
        "lite": False,
        "with_zlib": False,
        "with_snappy": False,
        "with_lz4": False,
        "with_zstd": False,
        "with_tbb": False,
        "enable_sse": False,
        "with_gflags": False,
        "with_jemalloc": False,
        "use_rtti": True,
   }

    def source(self):
        # Download and extract the source code
        tools.get(f"https://github.com/facebook/rocksdb/archive/refs/tags/v{self.version}.tar.gz")
        os.rename(f"rocksdb-{self.version}", "source_folder")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["WITH_LIBURING"] = "OFF"
        cmake.definitions["FAIL_ON_WARNINGS"] = "OFF"
        cmake.definitions["WITH_BENCHMARK_TOOLS"] = "OFF"
        cmake.definitions["WITH_SNAPPY"] = "OFF"
        cmake.definitions["WITH_LZ4"] = "OFF"
        cmake.definitions["WITH_GFLAGS"] = "OFF"
        cmake.definitions["WITH_JEMALLOC"] = "OFF"
        cmake.definitions["USE_RTTI"] = "1"
        cmake.definitions["PORTABLE"] = "ON"
        cmake.definitions["FORCE_SSE42"] = "OFF"
        cmake.definitions["BUILD_SHARED"] = "OFF"
        cmake.definitions["WITH_TESTS"] = "OFF"
        cmake.definitions["WITH_TOOLS"] = "OFF"
        cmake.definitions["CMAKE_ENABLE_SHARED"] = "OFF"
        cmake.configure(source_folder="source_folder")
        cmake.build()



    def _remove_shared_libraries(self):
        for shared_lib_name in ["lib*.so", "lib.so.*"]:
            tools.remove_files_by_mask(os.path.join(self.package_folder, "lib"), shared_lib_name)



    def package(self):
       cmake = CMake(self)
       cmake.install()
#        self.copy("*.h", dst="include", src="source_folder/include")
       self.copy("*.a", dst="lib", src="source_folder", keep_path=False)
       if self.options.shared is False:
            self._remove_shared_libraries()
#        self.copy("*.so*", dst="lib", src="source_folder", keep_path=False)
#        self.copy("*.dylib*", dst="lib", src="source_folder", keep_path=False)
#        self.copy("*.lib", dst="lib", src="source_folder", keep_path=False)
#        self.copy("*.dll", dst="bin", src="source_folder", keep_path=False)



    def package_info(self):
        cmake_target = "rocksdb-shared" if self.options.shared else "rocksdb"
        self.cpp_info.set_property("cmake_file_name", "RocksDB")
        self.cpp_info.set_property("cmake_target_name", "RocksDB::{}".format(cmake_target))
        # TODO: back to global scope in conan v2 once cmake_find_package* generators removed
        self.cpp_info.components["librocksdb"].libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.components["librocksdb"].system_libs = ["shlwapi", "rpcrt4"]
            if self.options.shared:
                self.cpp_info.components["librocksdb"].defines = ["ROCKSDB_DLL"]
        elif self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["librocksdb"].system_libs = ["pthread", "m"]
        if self.options.lite:
            self.cpp_info.components["librocksdb"].defines.append("ROCKSDB_LITE")
        # TODO: to remove in conan v2 once cmake_find_package* generators removed
        self.cpp_info.names["cmake_find_package"] = "RocksDB"
        self.cpp_info.names["cmake_find_package_multi"] = "RocksDB"
        self.cpp_info.components["librocksdb"].names["cmake_find_package"] = cmake_target
        self.cpp_info.components["librocksdb"].names["cmake_find_package_multi"] = cmake_target
        self.cpp_info.components["librocksdb"].set_property("cmake_target_name", "RocksDB::{}".format(cmake_target))
        if self.options.with_gflags:
            self.cpp_info.components["librocksdb"].requires.append("gflags::gflags")
        if self.options.with_snappy:
            self.cpp_info.components["librocksdb"].requires.append("snappy::snappy")
        if self.options.with_lz4:
            self.cpp_info.components["librocksdb"].requires.append("lz4::lz4")
        if self.options.with_zlib:
            self.cpp_info.components["librocksdb"].requires.append("zlib::zlib")
        if self.options.with_zstd:
            self.cpp_info.components["librocksdb"].requires.append("zstd::zstd")
        if self.options.get_safe("with_tbb"):
            self.cpp_info.components["librocksdb"].requires.append("onetbb::onetbb")
        if self.options.with_jemalloc:
            self.cpp_info.components["librocksdb"].requires.append("jemalloc::jemalloc")
