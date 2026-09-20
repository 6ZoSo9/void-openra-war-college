#pragma once

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef void* void_openbw_casc_storage;
typedef void* void_openbw_casc_file;

int void_openbw_casc_open_storage(
    const char* root,
    void_openbw_casc_storage* out_storage);

void void_openbw_casc_close_storage(
    void_openbw_casc_storage storage);

int void_openbw_casc_open_file(
    void_openbw_casc_storage storage,
    const char* filename,
    void_openbw_casc_file* out_file);

int void_openbw_casc_file_size(
    void_openbw_casc_file file,
    uint64_t* out_size);

int void_openbw_casc_read_file(
    void_openbw_casc_file file,
    void* destination,
    uint32_t bytes_to_read,
    uint32_t* out_bytes_read);

void void_openbw_casc_close_file(
    void_openbw_casc_file file);

#ifdef __cplusplus
}
#endif
