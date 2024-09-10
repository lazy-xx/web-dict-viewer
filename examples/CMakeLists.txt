#imgui-ws自带示例的编译，因为imgui-ws的imgui降低了版本，该项目编译不了
# if (IMGUI_WS_BUILD_EXAMPLES_NULL)
#     add_subdirectory(basic-null)
#     add_subdirectory(demo-null)
#     add_subdirectory(textures-null)
# endif()

# if (IMGUI_WS_SUPPORT_SDL2 AND IMGUI_WS_BUILD_EXAMPLES_SDL2)
#     add_subdirectory(basic-sdl2)
# endif()

pybind11_add_module(PyWS PyWS.cpp)
set_target_properties(PyWS PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_compile_options(PyWS PRIVATE "-fPIC")
target_include_directories(PyWS PRIVATE ../include ../../third-party/imgui ../../include ../../src)
target_link_libraries(PyWS PRIVATE 
        imgui 
        imgui-ws 
        ${CMAKE_DL_LIBS}
        ${CMAKE_THREAD_LIBS_INIT}
)


