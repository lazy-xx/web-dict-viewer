if (IMGUI_WS_ALL_WARNINGS)
    if (CMAKE_COMPILER_IS_GNUCC OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pedantic")
    else()
        # todo : windows
    endif()
endif()

file(READ "imgui-ws.js" src_imgui-ws_js)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/common.h.in ${CMAKE_CURRENT_SOURCE_DIR}/common.h @ONLY)

add_library(imgui-ws ${IMTUI_LIBRARY_TYPE}
    imgui-ws.cpp
    compressor-xor-rle-per-draw-list.cpp
    compressor-xor-rle-per-draw-list-with-vtx-offset.cpp
    )
set_target_properties(imgui-ws PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_compile_options(imgui-ws PRIVATE "-fPIC")
target_include_directories(imgui-ws PUBLIC
    ../include
    )

target_link_libraries(imgui-ws PRIVATE
    imgui
    incppect
    ${CMAKE_DL_LIBS}
    ${CMAKE_THREAD_LIBS_INIT}
    )
