#include <CascLib.h>

#include <algorithm>
#include <cctype>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <string>
#include <vector>

namespace {

std::string normalize(std::string value) {
  std::replace(value.begin(), value.end(), '\\', '/');
  std::transform(
      value.begin(),
      value.end(),
      value.begin(),
      [](unsigned char ch) { return static_cast<char>(std::tolower(ch)); });
  return value;
}

bool ends_with(const std::string& value, const std::string& suffix) {
  return value.size() >= suffix.size() &&
         value.compare(value.size() - suffix.size(), suffix.size(), suffix) == 0;
}

const std::vector<std::string> kCriticalSuffixes = {
    "arr/units.dat",
    "arr/weapons.dat",
    "arr/flingy.dat",
    "arr/sprites.dat",
    "arr/images.dat",
    "arr/orders.dat",
    "arr/techdata.dat",
    "arr/upgrades.dat",
    "arr/sfxdata.dat",
    "arr/sfxdata.tbl",
    "tileset/badlands.cv5",
    "tileset/badlands.vf4",
    "tileset/badlands.vx4",
    "tileset/badlands.vr4",
    "tileset/badlands.wpe",
};

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: openbw_online_casc_metadata_probe <cache_dir>\n";
    return 64;
  }

  const std::string cache = argv[1];
  if (cache.empty() || cache.find(':') != std::string::npos) {
    std::cerr << "HOLD=cache_path_invalid\n";
    return 65;
  }

  const std::string params = cache + ":s1:us";
  HANDLE storage = nullptr;

  std::cout << "schema=void.war-college.openbw-online-casc-metadata-probe.v1\n";
  std::cout << "product_requested=s1\n";
  std::cout << "region_requested=us\n";
  std::cout << "locale_requested=enUS\n";
  std::cout << "file_payload_open=false\n";
  std::cout << "game_execution=false\n";
  std::cout << "battle_net_execution=false\n";
  std::cout << "openbw_execution=false\n";

  if (!CascOpenOnlineStorage(params.c_str(), CASC_LOCALE_ENUS, &storage) ||
      storage == nullptr) {
    std::cerr << "HOLD=CascOpenOnlineStorage_failed\n";
    std::cerr << "casc_error=" << GetCascError() << "\n";
    return 66;
  }

  CASC_STORAGE_PRODUCT product{};
  size_t product_bytes = 0;
  if (!CascGetStorageInfo(
          storage,
          CascStorageProduct,
          &product,
          sizeof(product),
          &product_bytes)) {
    std::cerr << "HOLD=CascStorageProduct_failed\n";
    std::cerr << "casc_error=" << GetCascError() << "\n";
    CascCloseStorage(storage);
    return 67;
  }

  DWORD features = 0;
  size_t feature_bytes = 0;
  if (!CascGetStorageInfo(
          storage,
          CascStorageFeatures,
          &features,
          sizeof(features),
          &feature_bytes)) {
    std::cerr << "HOLD=CascStorageFeatures_failed\n";
    std::cerr << "casc_error=" << GetCascError() << "\n";
    CascCloseStorage(storage);
    return 68;
  }

  DWORD total_files = 0;
  size_t total_file_bytes = 0;
  if (!CascGetStorageInfo(
          storage,
          CascStorageTotalFileCount,
          &total_files,
          sizeof(total_files),
          &total_file_bytes)) {
    std::cerr << "HOLD=CascStorageTotalFileCount_failed\n";
    std::cerr << "casc_error=" << GetCascError() << "\n";
    CascCloseStorage(storage);
    return 69;
  }

  std::cout << "product_observed=" << product.szCodeName << "\n";
  std::cout << "build_number=" << product.BuildNumber << "\n";
  std::cout << "storage_features=0x" << std::hex << features << std::dec << "\n";
  std::cout << "storage_total_file_count=" << total_files << "\n";
  std::cout << "storage_online_feature="
            << ((features & CASC_FEATURE_ONLINE) ? "true" : "false") << "\n";
  std::cout << "storage_file_names_feature="
            << ((features & CASC_FEATURE_FILE_NAMES) ? "true" : "false") << "\n";

  CASC_FIND_DATA find_data{};
  HANDLE finder = CascFindFirstFile(storage, "*", &find_data, nullptr);
  if (finder == INVALID_HANDLE_VALUE) {
    std::cerr << "HOLD=CascFindFirstFile_failed\n";
    std::cerr << "casc_error=" << GetCascError() << "\n";
    CascCloseStorage(storage);
    return 70;
  }

  std::set<std::string> matched_suffixes;
  std::vector<std::string> matched_names;
  std::uint64_t enumerated = 0;
  constexpr std::uint64_t kEnumerationCap = 1000000;

  do {
    ++enumerated;
    if (enumerated > kEnumerationCap) {
      CascFindClose(finder);
      CascCloseStorage(storage);
      std::cerr << "HOLD=enumeration_cap_exceeded\n";
      return 71;
    }

    const std::string original = find_data.szFileName;
    const std::string name = normalize(original);

    for (const auto& suffix : kCriticalSuffixes) {
      if (ends_with(name, suffix) && matched_suffixes.insert(suffix).second) {
        matched_names.push_back(original);
      }
    }
  } while (CascFindNextFile(finder, &find_data));

  CascFindClose(finder);
  CascCloseStorage(storage);

  std::cout << "enumerated_file_count=" << enumerated << "\n";
  std::cout << "critical_suffix_count=" << kCriticalSuffixes.size() << "\n";
  std::cout << "critical_match_count=" << matched_suffixes.size() << "\n";

  for (const auto& name : matched_names) {
    std::cout << "critical_match=" << name << "\n";
  }

  for (const auto& suffix : kCriticalSuffixes) {
    if (matched_suffixes.count(suffix) == 0) {
      std::cout << "critical_missing_suffix=" << suffix << "\n";
    }
  }

  std::cout << "file_payload_open=false\n";
  std::cout << "file_payload_read=false\n";
  std::cout << "terminal=OPENBW_S1_ONLINE_CASC_METADATA_GREEN\n";
  return 0;
}
