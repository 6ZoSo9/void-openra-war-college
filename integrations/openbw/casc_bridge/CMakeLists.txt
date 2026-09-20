cmake_minimum_required(VERSION 3.16)
project(VoidOpenBWCascBridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT DEFINED VOID_CASCLIB_INSTALL_ROOT)
  message(FATAL_ERROR "VOID_CASCLIB_INSTALL_ROOT is required")
endif()

set(CASC_INCLUDE_DIR "${VOID_CASCLIB_INSTALL_ROOT}/include")
set(CASC_LIBRARY "${VOID_CASCLIB_INSTALL_ROOT}/lib/libcasc.so")

if(NOT EXISTS "${CASC_INCLUDE_DIR}/CascLib.h")
  message(FATAL_ERROR "CascLib.h missing")
endif()
if(NOT EXISTS "${CASC_LIBRARY}")
  message(FATAL_ERROR "libcasc.so missing")
endif()

add_library(void_openbw_casc_bridge SHARED
  void_openbw_casc_bridge.cpp
)

target_include_directories(void_openbw_casc_bridge
  PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}"
  PRIVATE "${CASC_INCLUDE_DIR}"
)

target_link_libraries(void_openbw_casc_bridge PRIVATE "${CASC_LIBRARY}")

set_target_properties(void_openbw_casc_bridge PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
  BUILD_RPATH "${VOID_CASCLIB_INSTALL_ROOT}/lib"
)
