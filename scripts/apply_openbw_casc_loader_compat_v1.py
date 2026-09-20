#!/usr/bin/env python3
"""Apply a transient CASC loader to exact pinned OpenBW/BWAPI.

CascLib itself remains behind a War College-owned C ABI shim so old BWAPI's
Windows-compatibility typedefs never collide with CascLib's typedefs.
No OpenBW or ChkForge source is vendored.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

OPENBW_DATA_LOADING = Path("data_loading.h")
BWAPI_OPENBWDATA_CMAKE = Path("bwapi/OpenBWData/CMakeLists.txt")

OPENBW_DATA_LOADING_PREIMAGE = "c8d5a0fd65a1672116189e9c95a7706e81f6671c"
BWAPI_OPENBWDATA_CMAKE_PREIMAGE = "4339d2300fefce5005ed57f49522d0ad66038019"

CASC_INCLUDE_ANCHOR = '#include <cstdio>\n\nnamespace bwgame {'
CASC_INCLUDE_REPLACEMENT = '#include <cstdio>\n#include "void_openbw_casc_bridge.h"\n#include <limits>\n\nnamespace bwgame {'

OLD_LOADER = r'''template<typename mpq_file_T = mpq_file<>>
struct data_files_loader {
	a_list<mpq_file_T> mpqs;

	void add_mpq_file(a_string filename) {
		mpqs.emplace_back(std::move(filename));
	}

	void operator()(a_vector<uint8_t>& dst, a_string filename) {
		for (auto& v : mpqs) {
			if (v.mpq.file_exists(filename)) {
				v(dst, std::move(filename));
				return;
			}
		}
		error("data_files_loader: %s: file not found", filename);
	}
};

template<typename data_files_loader_T = data_files_loader<>>
data_files_loader_T data_files_directory(a_string path) {
	if (!path.empty() && path[path.size() - 1] != '/' && path[path.size() - 1] != '\\') path += '/';
	data_files_loader_T r;
	r.add_mpq_file(path + "Patch_rt.mpq");
	r.add_mpq_file(path + "BrooDat.mpq");
	r.add_mpq_file(path + "StarDat.mpq");
	return r;
}
'''

NEW_LOADER = r'''struct casc_file_loader {
	void_openbw_casc_storage storage = nullptr;
	a_string root;

	casc_file_loader() = default;
	explicit casc_file_loader(a_string path) {
		open(std::move(path));
	}
	~casc_file_loader() {
		if (storage) void_openbw_casc_close_storage(storage);
	}
	casc_file_loader(const casc_file_loader&) = delete;
	casc_file_loader& operator=(const casc_file_loader&) = delete;
	casc_file_loader(casc_file_loader&& other) noexcept
		: storage(other.storage), root(std::move(other.root)) {
		other.storage = nullptr;
	}
	casc_file_loader& operator=(casc_file_loader&& other) noexcept {
		if (this != &other) {
			if (storage) void_openbw_casc_close_storage(storage);
			storage = other.storage;
			root = std::move(other.root);
			other.storage = nullptr;
		}
		return *this;
	}

	void open(a_string path) {
		if (storage) {
			void_openbw_casc_close_storage(storage);
			storage = nullptr;
		}
		root = std::move(path);
		if (!void_openbw_casc_open_storage(root.c_str(), &storage) || !storage) {
			error("casc_file_loader: failed to open CASC storage: %s", root);
		}
	}

	void operator()(a_vector<uint8_t>& dst, a_string filename) {
		if (!storage) error("casc_file_loader: storage not open");

		void_openbw_casc_file file = nullptr;
		if (!void_openbw_casc_open_file(storage, filename.c_str(), &file) || !file) {
			error("casc_file_loader: %s: file not found", filename);
		}

		uint64_t size64 = 0;
		if (!void_openbw_casc_file_size(file, &size64)) {
			void_openbw_casc_close_file(file);
			error("casc_file_loader: %s: failed to get size", filename);
		}
		if (size64 > std::numeric_limits<uint32_t>::max() || size64 > std::numeric_limits<size_t>::max()) {
			void_openbw_casc_close_file(file);
			error("casc_file_loader: %s: file too large", filename);
		}

		dst.resize((size_t)size64);
		uint32_t bytes_read = 0;
		if (!void_openbw_casc_read_file(file, dst.data(), (uint32_t)size64, &bytes_read)) {
			void_openbw_casc_close_file(file);
			error("casc_file_loader: %s: read failed", filename);
		}
		void_openbw_casc_close_file(file);
		if ((uint64_t)bytes_read != size64) {
			error("casc_file_loader: %s: short read", filename);
		}
	}
};

template<typename casc_file_loader_T = casc_file_loader>
struct data_files_loader {
	casc_file_loader_T casc;

	void open_casc_storage(a_string path) {
		casc.open(std::move(path));
	}

	void operator()(a_vector<uint8_t>& dst, a_string filename) {
		casc(dst, std::move(filename));
	}
};

template<typename data_files_loader_T = data_files_loader<>>
data_files_loader_T data_files_directory(a_string path) {
	data_files_loader_T r;
	r.open_casc_storage(std::move(path));
	return r;
}
'''

CMAKE_LINK_ANCHOR = '''if (OPENBW_ENABLE_UI)
  target_link_libraries(OpenBWData openbw_ui)
endif()

if (NOT WIN32)
'''
CMAKE_LINK_REPLACEMENT = '''if (OPENBW_ENABLE_UI)
  target_link_libraries(OpenBWData openbw_ui)
endif()

if (NOT DEFINED VOID_CASC_BRIDGE_SOURCE_ROOT)
  message(FATAL_ERROR "VOID_CASC_BRIDGE_SOURCE_ROOT is required for the transient CASC loader probe")
endif()
if (NOT DEFINED VOID_CASC_BRIDGE_BUILD_ROOT)
  message(FATAL_ERROR "VOID_CASC_BRIDGE_BUILD_ROOT is required for the transient CASC loader probe")
endif()
target_include_directories(OpenBWData PRIVATE "${VOID_CASC_BRIDGE_SOURCE_ROOT}")
target_link_libraries(OpenBWData "${VOID_CASC_BRIDGE_BUILD_ROOT}/lib/libvoid_openbw_casc_bridge.so")

if (NOT WIN32)
'''


class Hold(RuntimeError):
    pass


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def require_exact_blob(path: Path, expected: str) -> str:
    data = path.read_bytes()
    observed = git_blob_sha1(data)
    if observed != expected:
        raise Hold(f"preimage_drift:{path}:{observed}")
    return data.decode("utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise Hold(f"anchor_count:{label}:{count}")
    return text.replace(old, new, 1)


def apply(openbw: Path, bwapi: Path) -> dict[str, str]:
    data_path = openbw / OPENBW_DATA_LOADING
    cmake_path = bwapi / BWAPI_OPENBWDATA_CMAKE

    data_text = require_exact_blob(data_path, OPENBW_DATA_LOADING_PREIMAGE)
    cmake_text = require_exact_blob(cmake_path, BWAPI_OPENBWDATA_CMAKE_PREIMAGE)

    data_text = replace_once(
        data_text,
        CASC_INCLUDE_ANCHOR,
        CASC_INCLUDE_REPLACEMENT,
        "openbw_casc_bridge_include",
    )
    data_text = replace_once(
        data_text,
        OLD_LOADER,
        NEW_LOADER,
        "openbw_data_files_loader",
    )
    cmake_text = replace_once(
        cmake_text,
        CMAKE_LINK_ANCHOR,
        CMAKE_LINK_REPLACEMENT,
        "bwapi_openbwdata_casc_bridge_link",
    )

    data_path.write_text(data_text, encoding="utf-8")
    cmake_path.write_text(cmake_text, encoding="utf-8")

    return {
        "openbw_data_loading_preimage": OPENBW_DATA_LOADING_PREIMAGE,
        "openbw_data_loading_postimage": git_blob_sha1(data_path.read_bytes()),
        "bwapi_openbwdata_cmake_preimage": BWAPI_OPENBWDATA_CMAKE_PREIMAGE,
        "bwapi_openbwdata_cmake_postimage": git_blob_sha1(cmake_path.read_bytes()),
        "loader": "WarCollegeCAbiBridgeToCascLib",
        "openbw_source_vendored": "false",
        "chkforge_source_used": "false",
        "casclib_header_included_by_openbw": "false",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--openbw", required=True)
    parser.add_argument("--bwapi", required=True)
    args = parser.parse_args()

    try:
        result = apply(Path(args.openbw).resolve(), Path(args.bwapi).resolve())
    except Hold as exc:
        print(f"OPENBW_CASC_LOADER_COMPAT_HOLD={exc}")
        return 2

    for key, value in result.items():
        print(f"{key}={value}")
    print("OPENBW_CASC_LOADER_COMPAT_GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
