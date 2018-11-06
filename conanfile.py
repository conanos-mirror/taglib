from conans import ConanFile, CMake, tools
import os
import stat
import fnmatch

class TaglibConan(ConanFile):
    name = "taglib"
    version = "1.11.1"
    description = "TagLib is a library for reading and editing the meta-data of several popular audio formats"
    url = "https://github.com/conanos/taglib"
    license = "LGPLv2_1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "zlib/1.2.11@conanos/dev"

    source_subfolder = "source_subfolder"

    def source(self):
        url_ = 'http://{0}.org/releases/{0}-{1}.tar.gz'.format(self.name, self.version)
        tools.get(url_)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

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
        
        print "------", self.package_folder, self.install_folder
        
        with tools.chdir(self.source_subfolder):
            cmake = CMake(self)
            cmake.definitions["CMAKE_INSTALL_PREFIX"] = '%s/builddir/install'%(os.getcwd())
            cmake.definitions["WITH_MP4"] = 'ON'
            cmake.definitions["WITH_ASF"] = 'ON'
            cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_Boost"] = 'TRUE'
            cmake.definitions["ZLIB_ROOT"] = self.deps_cpp_info["zlib"].rootpath
            #cmake.definitions["CMAKE_C_COMPILER"] = 'gcc'
            #cmake.definitions["CMAKE_CXX_COMPILER"] = 'g++'
            #cmake.definitions["CMAKE_C_FLAGS"] = '-Wall -g -O2 -m64  -Wall -g -O2 -m64  -Wall -g -O2 -m64'
            #cmake.definitions["CMAKE_CXX_FLAGS"] = '-Wall -g -O2 -m64  -Wall -g -O2 -m64  -Wall -g -O2 -m64'
            if self.options.shared:
                cmake.definitions["BUILD_SHARED_LIBS"] = 1
            else:
                cmake.definitions["BUILD_STATIC_LIBS"] = 1
            cmake.configure(source_folder=self.source_subfolder,
                            build_folder='%s/builddir'%(self.source_subfolder))
            cmake.build()
            cmake.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir/install"%(os.getcwd()))

    def package_info(self):
        #self.cpp_info.libs = ["taglib"]
        self.cpp_info.libs = tools.collect_libs(self)

