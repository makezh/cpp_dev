# ==============================================================================
# I | General project settings
# ==============================================================================
cmake_minimum_required(VERSION 3.8)
set(project_name parse_json)
project(${project_name})


set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -Wall -Wextra -Wpedantic")

# ==============================================================================
# II | Preinstall settings
# ==============================================================================

# ------------------------------------------------------------------------------
# 1 | Include subdirectories
# ------------------------------------------------------------------------------
add_subdirectory(parse_json_lib)

message("PARSE_JSON_INCLUDE_DIRS = ${LIB_INCLUDE_DIRS}")
include(ExternalProject)

# ------------------------------------------------------------------------------
# 2 | Executable Main
# ------------------------------------------------------------------------------

add_executable(${PROJECT_NAME} src/main.cpp)
target_include_directories(${PROJECT_NAME} PUBLIC ${LIB_INCLUDE_DIRS})

option(BUILD_DYNAMIC "USING SHARED LIBRARY" OFF) # By default PARALLEL is OFF.
if(BUILD_DYNAMIC)
    message("PARSE_JSON_DYNAMIC_LIB = ${DYNAMIC_LIB}")
    target_link_libraries(${PROJECT_NAME} PUBLIC ${DYNAMIC_LIB})
else()
    message("PARSE_JSON_STATIC_LIB = ${STATIC_LIB}")
    target_link_libraries(${PROJECT_NAME} PUBLIC ${STATIC_LIB})
endif()
    
# ==============================================================================
# III | Check settings
# ==============================================================================

# ------------------------------------------------------------------------------
# 1 | Clang-Tidy
# ------------------------------------------------------------------------------
if(ENABLE_CLANG_TIDY)

    find_program(CLANG_TIDY_BIN clang-tidy-10)
    find_program(RUN_CLANG_TIDY_BIN run-clang-tidy-10.py)

    if(CLANG_TIDY_BIN STREQUAL "CLANG_TIDY_BIN-NOTFOUND")
        message(FATAL_ERROR "unable to locate clang-tidy-10")
    endif()

    if(RUN_CLANG_TIDY_BIN STREQUAL "RUN_CLANG_TIDY_BIN-NOTFOUND")
        message(FATAL_ERROR "unable to locate run-clang-tidy-10.py")
    endif()

    list(APPEND RUN_CLANG_TIDY_BIN_ARGS
        -clang-tidy-binary ${CLANG_TIDY_BIN}
        -header-filter=.*
        -checks=misc*,perf*,cppc*,read*,mode*
    )
    add_custom_target(
        tidy
        COMMAND ${RUN_CLANG_TIDY_BIN} ${RUN_CLANG_TIDY_BIN_ARGS}
        COMMENT "running clang tidy"
    )
endif()

# ------------------------------------------------------------------------------
# 2 | Clang-Format
# ------------------------------------------------------------------------------
if(ENABLE_CLANG_FORMAT)
  file(GLOB_RECURSE ALL_CXX_SOURCE_FILES
         ${PROJECT_SOURCE_DIR}/exe/main.cpp
         ${PROJECT_SOURCE_DIR}/parse_json_lib/*.hpp
         ${PROJECT_SOURCE_DIR}/parse_json_lib/*.cpp
         ${PROJECT_SOURCE_DIR}/test/*.cpp
  )
  add_custom_target(
    clang-format
    COMMAND /usr/bin/clang-format
    -i
    -style=Google
    ${ALL_CXX_SOURCE_FILES}
  )

endif()

# ------------------------------------------------------------------------------
# 3 | Facebook Infer
# ------------------------------------------------------------------------------
if(ENABLE_INFER)
  add_custom_target(
    infer
    COMMAND /usr/local/bin/infer run
    --reactive
    --print-logs
    --compilation-database compile_commands.json
  )
endif()

# ------------------------------------------------------------------------------
# 4 | CppLint
# ------------------------------------------------------------------------------
if(ENABLE_CPPLINT)
  file(GLOB_RECURSE ALL_CXX_SOURCE_FILES
        ${PROJECT_SOURCE_DIR}/exe/main.cpp
        ${PROJECT_SOURCE_DIR}/parse_json_lib/*.hpp
        ${PROJECT_SOURCE_DIR}/parse_json_lib/*.cpp
        ${PROJECT_SOURCE_DIR}/test/*.cpp
  )

  add_custom_target(
      cpplint
      COMMAND /usr/local/bin/cpplint 
      --extensions=c,cpp,h,hpp
      --linelength=80
      --filter=-runtime/casting,-runtime/arrays,-readability/casting,-build/include_subdir,-build/include_order,-whitespace/indent,-build/include_what_you_use,-runtime/printf
      ${ALL_CXX_SOURCE_FILES}
  )
endif()

# ------------------------------------------------------------------------------
# 5 | CodeCoverage
# ------------------------------------------------------------------------------
if(ENABLE_COVERAGE)
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -lgcov --coverage")
    set(CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS} -g -O0 -fprofile-arcs -ftest-coverage -lgcov")
endif()

# ------------------------------------------------------------------------------
# 6 | CppCheck
# ------------------------------------------------------------------------------
option(ENABLE_CPPCHECK "Build all tests." OFF) # Makes boolean 'test' available.
if(ENABLE_CPPCHECK)

    list(APPEND CPPCHECK_CMAKE_ARGS
        "-DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}"
    )

    ExternalProject_Add(
        cppcheck
        GIT_REPOSITORY      https://github.com/danmar/cppcheck.git
        GIT_TAG             1.79
        GIT_SHALLOW         1
        CMAKE_ARGS          ${CPPCHECK_CMAKE_ARGS}
        PREFIX              ${CMAKE_BINARY_DIR}/external/cppcheck/prefix
        TMP_DIR             ${CMAKE_BINARY_DIR}/external/cppcheck/tmp
        STAMP_DIR           ${CMAKE_BINARY_DIR}/external/cppcheck/stamp
        DOWNLOAD_DIR        ${CMAKE_BINARY_DIR}/external/cppcheck/download
        SOURCE_DIR          ${CMAKE_BINARY_DIR}/external/cppcheck/src
        BINARY_DIR          ${CMAKE_BINARY_DIR}/external/cppcheck/build
    )

    list(APPEND CPPCHECK_ARGS
        --enable=all
        --suppress=missingIncludeSystem
        --std=c11
        --verbose
        --error-exitcode=1
        --language=c
        --check-config
        -DMAIN=main
        -I ${CMAKE_SOURCE_DIR}/parse_json_lib
           ${CMAKE_SOURCE_DIR}/parse_json_lib/*.cpp
           ${CMAKE_SOURCE_DIR}/parse_json_lib/*.hpp
           ${CMAKE_SOURCE_DIR}/test/*.cpp
           ${CMAKE_SOURCE_DIR}/exe/main.cpp
    )

    add_custom_target(
        check
        COMMAND ${CMAKE_BINARY_DIR}/bin/cppcheck ${CPPCHECK_ARGS}
        COMMENT "running cppcheck"
    )
endif()


# ------------------------------------------------------------------------------
# 7 | Google Sanitizers
# ------------------------------------------------------------------------------
if(ENABLE_ASAN)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O1")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fuse-ld=gold")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-omit-frame-pointer")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=leak")
endif()

if(ENABLE_USAN)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fuse-ld=gold")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=undefined")
endif()

if(ENABLE_TSAN)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fuse-ld=gold")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=thread")
endif()


# ------------------------------------------------------------------------------
# 8 | Scan-build
# ------------------------------------------------------------------------------
if(ENABLE_SCAN_BUILD)
  file(GLOB_RECURSE ALL_CXX_SOURCE_FILES
        ${PROJECT_SOURCE_DIR}/exe/main.cpp
        ${PROJECT_SOURCE_DIR}/parse_json_lib/*.hpp
        ${PROJECT_SOURCE_DIR}/parse_json_lib/*.cpp
        ${PROJECT_SOURCE_DIR}/test/*.cpp
  )
  add_custom_target(
    scanbuild
    COMMAND analyze-build 
    --cdb compile_commands.json
    --use-analyzer /usr/bin/clang
    --output scan_answer.txt
    ${ALL_CXX_SOURCE_FILES}
  )
endif()

# ==============================================================================
# IV | Tests
# ==============================================================================

# ------------------------------------------------------------------------------
# 1 | Unit tests
# ------------------------------------------------------------------------------
option(BUILD_TESTS "Build all tests." OFF) # Makes boolean 'unit_test' available.

if(BUILD_TESTS)
    add_subdirectory(test)
endif()