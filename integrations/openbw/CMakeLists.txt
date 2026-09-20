cmake_minimum_required(VERSION 3.16)
project(VoidWarCollegeOpenBWSmokeBots LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT DEFINED BWAPI_SOURCE_ROOT)
  message(FATAL_ERROR "BWAPI_SOURCE_ROOT is required")
endif()
if(NOT DEFINED BWAPI_BUILD_ROOT)
  message(FATAL_ERROR "BWAPI_BUILD_ROOT is required")
endif()

set(BWAPI_INCLUDE_DIR "${BWAPI_SOURCE_ROOT}/bwapi/include")
set(BWAPILIB_PATH "${BWAPI_BUILD_ROOT}/lib/libBWAPILIB.so")

if(NOT EXISTS "${BWAPI_INCLUDE_DIR}/BWAPI.h")
  message(FATAL_ERROR "BWAPI headers missing")
endif()
if(NOT EXISTS "${BWAPILIB_PATH}")
  message(FATAL_ERROR "libBWAPILIB.so missing")
endif()

function(add_void_openbw_smoke_bot target role)
  add_library(${target} SHARED neutral_smoke_bot.cpp)
  target_compile_definitions(${target} PRIVATE VOID_OPENBW_SMOKE_ROLE=${role})
  target_include_directories(${target} PRIVATE "${BWAPI_INCLUDE_DIR}")
  target_link_libraries(${target} PRIVATE "${BWAPILIB_PATH}")
  set_target_properties(${target} PROPERTIES
    PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
  )
endfunction()

add_void_openbw_smoke_bot(VoidOpenBWSmokeBotA 0)
add_void_openbw_smoke_bot(VoidOpenBWSmokeBotB 1)
