#include "void_openbw_casc_bridge.h"

#include <CascLib.h>

extern "C" {

int void_openbw_casc_open_storage(
    const char* root,
    void_openbw_casc_storage* out_storage) {
  if (root == nullptr || out_storage == nullptr) return 0;
  HANDLE storage = nullptr;
  if (!CascOpenStorage(root, CASC_LOCALE_ALL, &storage) || storage == nullptr) {
    return 0;
  }
  *out_storage = storage;
  return 1;
}

void void_openbw_casc_close_storage(
    void_openbw_casc_storage storage) {
  if (storage != nullptr) CascCloseStorage((HANDLE)storage);
}

int void_openbw_casc_open_file(
    void_openbw_casc_storage storage,
    const char* filename,
    void_openbw_casc_file* out_file) {
  if (storage == nullptr || filename == nullptr || out_file == nullptr) return 0;
  HANDLE file = nullptr;
  if (!CascOpenFile(
          (HANDLE)storage,
          filename,
          CASC_LOCALE_ALL,
          CASC_OPEN_BY_NAME,
          &file) ||
      file == nullptr) {
    return 0;
  }
  *out_file = file;
  return 1;
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

void void_openbw_casc_close_file(
    void_openbw_casc_file file) {
  if (file != nullptr) CascCloseFile((HANDLE)file);
}

}  // extern "C"
