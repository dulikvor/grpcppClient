if (NOT PyCppConn_FOUND)

    ExternalProject_Add(PyCppConn
            GIT_REPOSITORY      https://github.com/Dudi119/Python_Cpp_Connectivity
            CONFIGURE_COMMAND   cd <SOURCE_DIR> && cmake .
            BUILD_COMMAND       cd <SOURCE_DIR> && make
            INSTALL_COMMAND     cp <SOURCE_DIR>/bin/libpyCppConn.so <INSTALL_DIR>/lib
            TEST_COMMAND        ""
            )

    ExternalProject_Add_Step(PyCppConn PyCppConn_Install_Headers
            COMMAND     mkdir -p <INSTALL_DIR>/include/pycppconn && sh -c "cp <SOURCE_DIR>/src/*.h <INSTALL_DIR>/include/pycppconn/"
            DEPENDEES   install
            )

    ExternalProject_Get_Property(PyCppConn INSTALL_DIR)

    set (PyCppConn_ROOT_DIR          ${INSTALL_DIR})
    set (PyCppConn_INCLUDE_DIR       ${PyCppConn_ROOT_DIR}/include)
    set (PyCppConn_FOUND             YES)

endif ()
