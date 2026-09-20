// VOID War College - neutral OpenBW smoke bot.
// Source-only plumbing probe. This is not Apollyon or Abaddon and performs no
// learning, model calls, filesystem I/O, network I/O, or hidden-information
// enablement.
//
// Build role 0: leave the match at a fixed frame to bound the future smoke run.
// Build role 1: remain passive so the two roles have a deterministic lifecycle.

#include <BWAPI.h>

#ifndef VOID_OPENBW_SMOKE_ROLE
#error "VOID_OPENBW_SMOKE_ROLE must be defined as 0 or 1"
#endif

#if VOID_OPENBW_SMOKE_ROLE != 0 && VOID_OPENBW_SMOKE_ROLE != 1
#error "VOID_OPENBW_SMOKE_ROLE must be 0 or 1"
#endif

namespace {

constexpr int kBoundedLeaveFrame = 480;

class VoidWarCollegeOpenBWSmokeBot final : public BWAPI::AIModule {
 public:
  void onStart() override {
    // Do not enable UserInput or CompleteMapInformation. Keep command handling
    // unoptimized so this probe does not change command grouping semantics.
    BWAPI::Broodwar->setCommandOptimizationLevel(0);
  }

  void onFrame() override {
    if (BWAPI::Broodwar->isReplay() ||
        BWAPI::Broodwar->isPaused() ||
        BWAPI::Broodwar->self() == nullptr) {
      return;
    }

#if VOID_OPENBW_SMOKE_ROLE == 0
    if (!leave_requested_ &&
        BWAPI::Broodwar->getFrameCount() >= kBoundedLeaveFrame) {
      leave_requested_ = true;
      BWAPI::Broodwar->leaveGame();
    }
#endif
  }

 private:
  bool leave_requested_ = false;
};

}  // namespace

extern "C" void gameInit(BWAPI::Game* game) {
  BWAPI::BroodwarPtr = game;
}

extern "C" BWAPI::AIModule* newAIModule() {
  return new VoidWarCollegeOpenBWSmokeBot();
}
