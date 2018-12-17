from conans import ConanFile, CMake, tools
from conanos.build import config_scheme
import os


class TaglibConan(ConanFile):
    name = "taglib"
    version = "1.11.1"
    description = "TagLib is a library for reading and editing the meta-data of several popular audio formats"
    url = "https://github.com/conanos/taglib"
    homepage = "https://taglib.org/"
    license = "LGPL-2.1"
    exports = ["COPYING.LGPL"]
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"

    requires = "zlib/1.2.11@conanos/stable"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        del self.settings.compiler.libcxx

        config_scheme(self)

    def source(self):
        url_ = 'https://taglib.org/releases/{name}-{version}.tar.gz'
        tools.get(url_.format(name=self.name, version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        #self.run('cmake -DCMAKE_INSTALL_PREFIX=%s/build -DCMAKE_LIBRARY_OUTPUT_PATH=%s/build/lib'
        #' -DWITH_MP4=ON -DWITH_ASF=ON -DBUILD_SHARED_LIBS=1 -DBUILD_STATIC_LIBS=1 -DCMAKE_DISABLE_FIND_PACKAGE_Boost=TRUE -DZLIB_ROOT=%s'
        #' -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_FLAGS=\" -Wall -g -O2 -m64  -Wall -g -O2 -m64  -Wall -g -O2 -m64 \"'
        #' -DCMAKE_CXX_FLAGS=\" -Wall -g -O2 -m64  -Wall -g -O2 -m64  -Wall -g -O2 -m64 \"'
        #' -DLIB_SUFFIX=  -DCMAKE_BUILD_TYPE=Release -DCMAKE_FIND_ROOT_PATH=%s'
        #%(os.getcwd(),os.getcwd(),self.deps_cpp_info["zlib"].rootpath,self.cerbero_root))
        #self.run('make -j4')
        #self.run('make install')
        # 
        
        with tools.chdir(self._source_subfolder):
            cmake = CMake(self)
            cmake.definitions["CMAKE_INSTALL_PREFIX"] = '%s/builddir/install'%(os.getcwd())
            cmake.definitions["WITH_MP4"] = 'ON'
            cmake.definitions["WITH_ASF"] = 'ON'
            cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_Boost"] = 'TRUE'
            cmake.definitions["ZLIB_ROOT"] = self.deps_cpp_info["zlib"].rootpath
            if self.options.shared:
                cmake.definitions["BUILD_SHARED_LIBS"] = 1
            else:
                cmake.definitions["BUILD_STATIC_LIBS"] = 1
            cmake.configure(source_folder=self._source_subfolder,
                            build_folder='%s/builddir'%(self._source_subfolder))
            cmake.build()
            cmake.install()

    def package(self):
        self.copy("*", src=os.path.join(self.build_folder, self._source_subfolder,"builddir","install"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

