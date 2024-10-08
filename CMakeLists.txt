cmake_minimum_required (VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
project(imgui-ws)

set(CMAKE_EXPORT_COMPILE_COMMANDS "on")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    set(IMGUI_WS_STANDALONE ON)
else()
    set(IMGUI_WS_STANDALONE OFF)
endif()

# options

option(IMGUI_WS_ALL_WARNINGS            "imgui-ws: enable all compiler warnings" ${IMGUI_WS_STANDALONE})
option(IMGUI_WS_ALL_WARNINGS_3RD_PARTY  "imgui-ws: enable all compiler warnings in 3rd party libs" OFF)

option(IMGUI_WS_SANITIZE_THREAD         "imgui-ws: enable thread sanitizer" OFF)
option(IMGUI_WS_SANITIZE_ADDRESS        "imgui-ws: enable address sanitizer" OFF)
option(IMGUI_WS_SANITIZE_UNDEFINED      "imgui-ws: enable undefined sanitizer" OFF)

option(IMGUI_WS_SUPPORT_SDL2            "imgui-ws: imgui with sdl2" OFF)

option(IMGUI_WS_BUILD_EXAMPLES_NULL     "imgui-ws: build headless examples" ${IMGUI_WS_STANDALONE})
option(IMGUI_WS_BUILD_EXAMPLES_SDL2     "imgui-ws: build sdl2 examples" ${IMGUI_WS_STANDALONE})

option(IMGUI_WS_BUILD_TOOLS             "imgui-ws: build tools" ${IMGUI_WS_STANDALONE})

# sanitizers

if (IMGUI_WS_SANITIZE_THREAD)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=thread")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=thread")
endif()

if (IMGUI_WS_SANITIZE_ADDRESS)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=address -fno-omit-frame-pointer")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address -fno-omit-frame-pointer")
endif()

if (IMGUI_WS_SANITIZE_UNDEFINED)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=undefined")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=undefined")
endif()

# dependencies

if (IMGUI_WS_SUPPORT_SDL2)
    find_package(OpenGL REQUIRED)
    find_package(SDL2 REQUIRED)
    string(STRIP "${SDL2_LIBRARIES}" SDL2_LIBRARIES)
endif()

# directories


include_directories(/usr/include/c++/11)
include_directories(/usr/include/x86_64-linux-gnu/c++/11)
include_directories(/usr/include/c++/11/backward)
include_directories(/usr/lib/gcc/x86_64-linux-gnu/11/include)
include_directories(/usr/local/include)
include_directories(/usr/include/x86_64-linux-gnu)
include_directories(/usr/include)

# main

find_package(Threads REQUIRED)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "RelWithDebInfo")
endif ()

add_subdirectory(extern/pybind11)
# pybind11_add_module(HelloWorld hello.cpp)
add_subdirectory(third-party)
add_subdirectory(src)

if (IMGUI_WS_STANDALONE)
    add_subdirectory(examples)
    add_subdirectory(tools)
endif()
