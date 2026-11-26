cmake_minimum_required(VERSION 3.16)
project(Pulse VERSION 0.1.0 LANGUAGES C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_library(pulse_core STATIC
    core/task.c memory/budget.c scheduler/run.c adaptive/width.c telemetry/json.c)
target_include_directories(pulse_core PUBLIC core)
target_compile_definitions(pulse_core PRIVATE _POSIX_C_SOURCE=200809L)
target_link_libraries(pulse_core PUBLIC Threads::Threads)

add_executable(pulse cli/main.c)
target_link_libraries(pulse PRIVATE pulse_core)

include(CTest)
if(BUILD_TESTING)
    add_executable(pulse_tests tests/test_pulse.c)
    target_link_libraries(pulse_tests PRIVATE pulse_core)
    add_test(NAME pulse_core COMMAND pulse_tests)
    add_test(NAME pulse_cli COMMAND ${CMAKE_COMMAND}
        -DPULSE=$<TARGET_FILE:pulse> -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/cli.cmake)
endif()
