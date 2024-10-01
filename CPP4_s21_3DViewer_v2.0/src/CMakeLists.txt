cmake_minimum_required(VERSION 3.5)

project(3DViewer_v2 VERSION 2.0.0 LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror")

# Before running CMake, set the environment variable QT_LIB_DIR
# with path to the Qt directory with libraries
set(CMAKE_PREFIX_PATH $ENV{QT_LIB_DIR})

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 REQUIRED COMPONENTS Widgets OpenGLWidgets OpenGL)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets OpenGLWidgets OpenGL)

file(GLOB_RECURSE MODEL_SOURCES "Model/*.cc" "Model/*.h")
file(GLOB_RECURSE VIEW_SOURCES "View/*.cc" "View/*.h" "View/*.ui" "View/*.qrc")
file(GLOB_RECURSE CONTROLLER_SOURCES "Controller/*.cc" "Controller/*.h")
file(GLOB_RECURSE QT_GIF_SOURCES "extern/gif-h/*.h" "extern/gif-h/*.c")

add_executable(3DViewer_v2 ${MODEL_SOURCES} ${VIEW_SOURCES} ${CONTROLLER_SOURCES} ${QT_GIF_SOURCES})

target_link_libraries(3DViewer_v2 PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)
target_link_libraries(3DViewer_v2 PRIVATE Qt${QT_VERSION_MAJOR}::OpenGLWidgets)
target_link_libraries(3DViewer_v2 PRIVATE Qt${QT_VERSION_MAJOR}::OpenGL)

include(GNUInstallDirs)
install(TARGETS 3DViewer_v2
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# Docs only available if this is the main app
# find_package(Doxygen)

# if(Doxygen_FOUND)
# add_subdirectory(docs)
# else()
# message(STATUS "Doxygen not found, not building docs")
# endif()
if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(3DViewer_v2)
endif()
