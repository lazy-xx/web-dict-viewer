set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
find_package(pybind11 REQUIRED)

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







