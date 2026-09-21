"""Deterministic source builder for the pinned OpenBW S1 CASC/VX4 lane.

No network, CASC, compiler, game or model action occurs by importing this module.
It transforms exact upstream source text and emits the bridge sources required by
an external build harness. Every replacement is single-count and fail-closed.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Mapping

OPENBW_COMMIT = "4b046d5f65302b10cb0a745f0fecd37ec85b20a8"
OPENBW_DATA_LOADING_PREIMAGE_BLOB = "c8d5a0fd65a1672116189e9c95a7706e81f6671c"
OPENBW_UI_PREIMAGE_BLOB = "aff631788c468af64fba10cf956e03fa35e35b02"
BWAPI_COMMIT = "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2"
BWAPI_OPENBWDATA_CMAKE_PREIMAGE_BLOB = "4339d2300fefce5005ed57f49522d0ad66038019"
CASCLIB_COMMIT = "2a280f5a231966dc5d1b534978dd9f9f04a374cd"
CASCLIB_HEADER_PREIMAGE_BLOB = "39e9d3bdf360940e165f7793c95acac5fe00a8ca"

PINNED_UPSTREAM_BLOBS = {
    "openbw/data_loading.h": OPENBW_DATA_LOADING_PREIMAGE_BLOB,
    "openbw/ui/ui.h": OPENBW_UI_PREIMAGE_BLOB,
    "bwapi/bwapi/OpenBWData/CMakeLists.txt": BWAPI_OPENBWDATA_CMAKE_PREIMAGE_BLOB,
    "casclib/src/CascLib.h": CASCLIB_HEADER_PREIMAGE_BLOB,
}

BRIDGE_HEADER_SOURCE = r'''#pragma once

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef void* void_openbw_casc_storage;
typedef void* void_openbw_casc_file;

int void_openbw_casc_open_storage(
    const char* root,
    int allow_download,
    void_openbw_casc_storage* out_storage);

void void_openbw_casc_close_storage(void_openbw_casc_storage storage);

int void_openbw_casc_open_file(
    void_openbw_casc_storage storage,
    const char* filename,
    void_openbw_casc_file* out_file);

uint32_t void_openbw_casc_last_error(void);
int void_openbw_casc_error_is_file_not_found(uint32_t error_code);

int void_openbw_casc_file_size(
    void_openbw_casc_file file,
    uint64_t* out_size);

int void_openbw_casc_read_file(
    void_openbw_casc_file file,
    void* destination,
    uint32_t bytes_to_read,
    uint32_t* out_bytes_read);

void void_openbw_casc_close_file(void_openbw_casc_file file);

#ifdef __cplusplus
}
#endif
'''

BRIDGE_CPP_SOURCE = r'''#include "void_openbw_casc_bridge.h"

#include <CascLib.h>

extern "C" {

int void_openbw_casc_open_storage(
    const char* root,
    int allow_download,
    void_openbw_casc_storage* out_storage) {
  if (root == nullptr || out_storage == nullptr) return 0;
  *out_storage = nullptr;

  CASC_OPEN_STORAGE_ARGS args{};
  args.Size = sizeof(args);
  args.szLocalPath = root;
  args.szCodeName = "s1";
  args.szRegion = "us";
  args.dwLocaleMask = CASC_LOCALE_ENUS;
  args.dwFlags = allow_download ? CASC_FEATURE_ALLOW_DOWNLOAD : 0;

  HANDLE storage = nullptr;
  if (!CascOpenStorageEx(nullptr, &args, true, &storage) || storage == nullptr) {
    return 0;
  }

  *out_storage = storage;
  return 1;
}

void void_openbw_casc_close_storage(void_openbw_casc_storage storage) {
  if (storage != nullptr) CascCloseStorage((HANDLE)storage);
}

int void_openbw_casc_open_file(
    void_openbw_casc_storage storage,
    const char* filename,
    void_openbw_casc_file* out_file) {
  if (storage == nullptr || filename == nullptr || out_file == nullptr) return 0;
  *out_file = nullptr;
  HANDLE file = nullptr;
  if (!CascOpenFile(
          (HANDLE)storage,
          filename,
          CASC_LOCALE_ENUS,
          CASC_OPEN_BY_NAME,
          &file) ||
      file == nullptr) {
    return 0;
  }
  *out_file = file;
  return 1;
}

uint32_t void_openbw_casc_last_error(void) {
  return (uint32_t)GetCascError();
}

int void_openbw_casc_error_is_file_not_found(uint32_t error_code) {
  return error_code == (uint32_t)ERROR_FILE_NOT_FOUND;
}

int void_openbw_casc_file_size(
    void_openbw_casc_file file,
    uint64_t* out_size) {
  if (file == nullptr || out_size == nullptr) return 0;
  ULONGLONG size = 0;
  if (!CascGetFileSize64((HANDLE)file, &size)) return 0;
  *out_size = (uint64_t)size;
  return 1;
}

int void_openbw_casc_read_file(
    void_openbw_casc_file file,
    void* destination,
    uint32_t bytes_to_read,
    uint32_t* out_bytes_read) {
  if (file == nullptr || out_bytes_read == nullptr) return 0;
  DWORD observed = 0;
  if (bytes_to_read != 0 &&
      !CascReadFile((HANDLE)file, destination, (DWORD)bytes_to_read, &observed)) {
    return 0;
  }
  *out_bytes_read = (uint32_t)observed;
  return 1;
}

void void_openbw_casc_close_file(void_openbw_casc_file file) {
  if (file != nullptr) CascCloseFile((HANDLE)file);
}

}  // extern "C"
'''

BRIDGE_CMAKE_SOURCE = r'''cmake_minimum_required(VERSION 3.16)
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

add_library(void_openbw_casc_bridge SHARED void_openbw_casc_bridge.cpp)
target_include_directories(void_openbw_casc_bridge
  PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}"
  PRIVATE "${CASC_INCLUDE_DIR}"
)
target_link_libraries(void_openbw_casc_bridge PRIVATE "${CASC_LIBRARY}")
set_target_properties(void_openbw_casc_bridge PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
  BUILD_RPATH "${VOID_CASCLIB_INSTALL_ROOT}/lib"
)
'''

DATA_LOADING_INCLUDE_OLD = '#include <cstdio>\n\nnamespace bwgame {'
DATA_LOADING_INCLUDE_NEW = (
    '#include <cstdio>\n'
    '#include "void_openbw_casc_bridge.h"\n'
    '#include <cstdlib>\n'
    '#include <limits>\n\n'
    'namespace bwgame {'
)

DATA_LOADING_LOADER_OLD = '''template<typename mpq_file_T = mpq_file<>>
struct data_files_loader {
\ta_list<mpq_file_T> mpqs;

\tvoid add_mpq_file(a_string filename) {
\t\tmpqs.emplace_back(std::move(filename));
\t}

\tvoid operator()(a_vector<uint8_t>& dst, a_string filename) {
\t\tfor (auto& v : mpqs) {
\t\t\tif (v.mpq.file_exists(filename)) {
\t\t\t\tv(dst, std::move(filename));
\t\t\t\treturn;
\t\t\t}
\t\t}
\t\terror("data_files_loader: %s: file not found", filename);
\t}
};

template<typename data_files_loader_T = data_files_loader<>>
data_files_loader_T data_files_directory(a_string path) {
\tif (!path.empty() && path[path.size() - 1] != '/' && path[path.size() - 1] != '\\\\') path += '/';
\tdata_files_loader_T r;
\tr.add_mpq_file(path + "Patch_rt.mpq");
\tr.add_mpq_file(path + "BrooDat.mpq");
\tr.add_mpq_file(path + "StarDat.mpq");
\treturn r;
}
'''

DATA_LOADING_LOADER_NEW = '''struct casc_file_loader {
\tvoid_openbw_casc_storage storage = nullptr;
\ta_string root;

\tcasc_file_loader() = default;
\texplicit casc_file_loader(a_string path) { open(std::move(path)); }
\t~casc_file_loader() {
\t\tif (storage) void_openbw_casc_close_storage(storage);
\t}
\tcasc_file_loader(const casc_file_loader&) = delete;
\tcasc_file_loader& operator=(const casc_file_loader&) = delete;
\tcasc_file_loader(casc_file_loader&& other) noexcept
\t\t: storage(other.storage), root(std::move(other.root)) {
\t\tother.storage = nullptr;
\t}
\tcasc_file_loader& operator=(casc_file_loader&& other) noexcept {
\t\tif (this != &other) {
\t\t\tif (storage) void_openbw_casc_close_storage(storage);
\t\t\tstorage = other.storage;
\t\t\troot = std::move(other.root);
\t\t\tother.storage = nullptr;
\t\t}
\t\treturn *this;
\t}

\tvoid open(a_string path) {
\t\tif (storage) {
\t\t\tvoid_openbw_casc_close_storage(storage);
\t\t\tstorage = nullptr;
\t\t}
\t\troot = std::move(path);
\t\tint allow_download = 0;
\t\tif (const char* v = std::getenv("VOID_OPENBW_CASC_ALLOW_DOWNLOAD")) {
\t\t\tallow_download = !std::strcmp(v, "1");
\t\t}
\t\tif (!void_openbw_casc_open_storage(root.c_str(), allow_download, &storage) || !storage) {
\t\t\terror("casc_file_loader: failed to open CASC storage: %s (error=%d)",
\t\t\t      root, void_openbw_casc_last_error());
\t\t}
\t}

\tvoid read_open_file(
\t\tvoid_openbw_casc_file file,
\t\ta_vector<uint8_t>& dst,
\t\tconst a_string& filename) {
\t\tuint64_t size64 = 0;
\t\tif (!void_openbw_casc_file_size(file, &size64)) {
\t\t\tuint32_t e = void_openbw_casc_last_error();
\t\t\tvoid_openbw_casc_close_file(file);
\t\t\terror("casc_file_loader: %s: failed to get size (error=%d)", filename, e);
\t\t}
\t\tif (size64 > std::numeric_limits<uint32_t>::max() ||
\t\t    size64 > std::numeric_limits<size_t>::max()) {
\t\t\tvoid_openbw_casc_close_file(file);
\t\t\terror("casc_file_loader: %s: file too large", filename);
\t\t}
\t\tdst.resize((size_t)size64);
\t\tuint32_t bytes_read = 0;
\t\tif (!void_openbw_casc_read_file(file, dst.data(), (uint32_t)size64, &bytes_read)) {
\t\t\tuint32_t e = void_openbw_casc_last_error();
\t\t\tvoid_openbw_casc_close_file(file);
\t\t\terror("casc_file_loader: %s: read failed (error=%d)", filename, e);
\t\t}
\t\tvoid_openbw_casc_close_file(file);
\t\tif ((uint64_t)bytes_read != size64) {
\t\t\terror("casc_file_loader: %s: short read", filename);
\t\t}
\t}

\tvoid operator()(a_vector<uint8_t>& dst, a_string filename) {
\t\tif (!storage) error("casc_file_loader: storage not open");

\t\tbool vx4_request = filename.size() >= 4 &&
\t\t\tfilename.compare(filename.size() - 4, 4, ".vx4") == 0;
\t\tif (vx4_request) {
\t\t\ta_string modern_name = filename + "ex";
\t\t\tvoid_openbw_casc_file modern = nullptr;
\t\t\tif (void_openbw_casc_open_file(storage, modern_name.c_str(), &modern) && modern) {
\t\t\t\tread_open_file(modern, dst, modern_name);
\t\t\t\tif (dst.size() % 64 != 0) {
\t\t\t\t\terror("casc_file_loader: %s: invalid VX4EX length %d", modern_name, dst.size());
\t\t\t\t}
\t\t\t\treturn;
\t\t\t}
\t\t\tuint32_t modern_error = void_openbw_casc_last_error();
\t\t\tif (!void_openbw_casc_error_is_file_not_found(modern_error)) {
\t\t\t\terror("casc_file_loader: %s: modern open failed (error=%d)",
\t\t\t\t      modern_name, modern_error);
\t\t\t}

\t\t\tvoid_openbw_casc_file classic_file = nullptr;
\t\t\tif (!void_openbw_casc_open_file(storage, filename.c_str(), &classic_file) || !classic_file) {
\t\t\t\terror("casc_file_loader: %s: classic open failed (error=%d)",
\t\t\t\t      filename, void_openbw_casc_last_error());
\t\t\t}
\t\t\ta_vector<uint8_t> classic;
\t\t\tread_open_file(classic_file, classic, filename);
\t\t\tif (classic.size() % 32 != 0) {
\t\t\t\terror("casc_file_loader: %s: invalid classic VX4 length %d", filename, classic.size());
\t\t\t}
\t\t\tdst.resize(classic.size() * 2);
\t\t\tfor (size_t src = 0, out = 0; src != classic.size(); src += 2, out += 4) {
\t\t\t\tuint16_t value = (uint16_t)classic[src] | (uint16_t)classic[src + 1] << 8;
\t\t\t\tdst[out] = (uint8_t)(value & 0xff);
\t\t\t\tdst[out + 1] = (uint8_t)(value >> 8);
\t\t\t\tdst[out + 2] = 0;
\t\t\t\tdst[out + 3] = 0;
\t\t\t}
\t\t\treturn;
\t\t}

\t\tvoid_openbw_casc_file file = nullptr;
\t\tif (!void_openbw_casc_open_file(storage, filename.c_str(), &file) || !file) {
\t\t\terror("casc_file_loader: %s: open failed (error=%d)",
\t\t\t      filename, void_openbw_casc_last_error());
\t\t}
\t\tread_open_file(file, dst, filename);
\t}
};

template<typename casc_file_loader_T = casc_file_loader>
struct data_files_loader {
\tcasc_file_loader_T casc;
\tvoid open_casc_storage(a_string path) { casc.open(std::move(path)); }
\tvoid operator()(a_vector<uint8_t>& dst, a_string filename) {
\t\tcasc(dst, std::move(filename));
\t}
};

template<typename data_files_loader_T = data_files_loader<>>
data_files_loader_T data_files_directory(a_string path) {
\tdata_files_loader_T r;
\tr.open_casc_storage(std::move(path));
\treturn r;
}
'''

UI_VX4_STRUCT_OLD = '''struct vx4_entry {
\tstd::array<uint16_t, 16> images;
};'''
UI_VX4_STRUCT_NEW = '''struct vx4_entry {
\tstd::array<uint32_t, 16> images;
};'''

UI_VX4_PARSE_OLD = '''data_reader<true, false> vx4_r(vx4_data.data(), vx4_data.data() + vx4_data.size());
\timg.vx4.resize(vx4_data.size() / 32);
\tfor (size_t i = 0; i != img.vx4.size(); ++i) {
\t\tfor (size_t i2 = 0; i2 != 16; ++i2) {
\t\t\timg.vx4[i].images[i2] = vx4_r.get<uint16_t>();
\t\t}
\t}'''
UI_VX4_PARSE_NEW = '''if (vx4_data.size() % 64 != 0) error("canonical vx4 data size invalid (%d)", vx4_data.size());
\tdata_reader<true, false> vx4_r(vx4_data.data(), vx4_data.data() + vx4_data.size());
\timg.vx4.resize(vx4_data.size() / 64);
\tfor (size_t i = 0; i != img.vx4.size(); ++i) {
\t\tfor (size_t i2 = 0; i2 != 16; ++i2) {
\t\t\timg.vx4[i].images[i2] = vx4_r.get<uint32_t>();
\t\t}
\t}'''

CMAKE_LINK_OLD = '''if (OPENBW_ENABLE_UI)
  target_link_libraries(OpenBWData openbw_ui)
endif()

if (NOT WIN32)
'''
CMAKE_LINK_NEW = '''if (OPENBW_ENABLE_UI)
  target_link_libraries(OpenBWData openbw_ui)
endif()

if (NOT DEFINED VOID_CASC_BRIDGE_SOURCE_ROOT)
  message(FATAL_ERROR "VOID_CASC_BRIDGE_SOURCE_ROOT is required")
endif()
if (NOT DEFINED VOID_CASC_BRIDGE_BUILD_ROOT)
  message(FATAL_ERROR "VOID_CASC_BRIDGE_BUILD_ROOT is required")
endif()
target_include_directories(OpenBWData PRIVATE "${VOID_CASC_BRIDGE_SOURCE_ROOT}")
target_link_libraries(OpenBWData "${VOID_CASC_BRIDGE_BUILD_ROOT}/lib/libvoid_openbw_casc_bridge.so")

if (NOT WIN32)
'''


class SourcePatchHold(RuntimeError):
    """Exact source identity/shape is not the admitted patch target."""


def git_blob_sha1(text: str) -> str:
    raw = text.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def _replace_exact(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise SourcePatchHold(f"{label}: expected exactly one anchor, observed {count}")
    return source.replace(old, new, 1)


def validate_upstream_blobs(observed: Mapping[str, str]) -> None:
    for path, expected in PINNED_UPSTREAM_BLOBS.items():
        actual = observed.get(path)
        if actual != expected:
            raise SourcePatchHold(f"upstream blob drift: {path}: {actual!r} != {expected}")


def patch_openbw_data_loading(source: str) -> str:
    patched = _replace_exact(
        source,
        DATA_LOADING_INCLUDE_OLD,
        DATA_LOADING_INCLUDE_NEW,
        "data_loading include",
    )
    return _replace_exact(
        patched,
        DATA_LOADING_LOADER_OLD,
        DATA_LOADING_LOADER_NEW,
        "data_loading loader",
    )


def patch_openbw_ui(source: str) -> str:
    patched = _replace_exact(source, UI_VX4_STRUCT_OLD, UI_VX4_STRUCT_NEW, "ui vx4 struct")
    return _replace_exact(patched, UI_VX4_PARSE_OLD, UI_VX4_PARSE_NEW, "ui vx4 parser")


def patch_bwapi_openbwdata_cmake(source: str) -> str:
    return _replace_exact(source, CMAKE_LINK_OLD, CMAKE_LINK_NEW, "OpenBWData bridge link")


@dataclass(frozen=True)
class SourcePatchBundle:
    data_loading: str
    ui_header: str
    openbwdata_cmake: str
    bridge_header: str = BRIDGE_HEADER_SOURCE
    bridge_cpp: str = BRIDGE_CPP_SOURCE
    bridge_cmake: str = BRIDGE_CMAKE_SOURCE

    def identities(self) -> dict[str, str]:
        return {
            "openbw/data_loading.h": git_blob_sha1(self.data_loading),
            "openbw/ui/ui.h": git_blob_sha1(self.ui_header),
            "bwapi/bwapi/OpenBWData/CMakeLists.txt": git_blob_sha1(self.openbwdata_cmake),
            "bridge/void_openbw_casc_bridge.h": git_blob_sha1(self.bridge_header),
            "bridge/void_openbw_casc_bridge.cpp": git_blob_sha1(self.bridge_cpp),
            "bridge/CMakeLists.txt": git_blob_sha1(self.bridge_cmake),
        }


def build_source_patch_bundle(
    *,
    data_loading: str,
    ui_header: str,
    openbwdata_cmake: str,
) -> SourcePatchBundle:
    return SourcePatchBundle(
        data_loading=patch_openbw_data_loading(data_loading),
        ui_header=patch_openbw_ui(ui_header),
        openbwdata_cmake=patch_bwapi_openbwdata_cmake(openbwdata_cmake),
    )
