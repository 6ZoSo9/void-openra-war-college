// VOID War College - bounded neutral OpenBW dual-local runtime smoke.
// Two local OpenBW instances, no learning/model calls, no hidden-information
// flags, and no unit commands. Role A requests leave at frame 480. Role B
// ignores anonymous startup PlayerLeft events, recognizes only the named VOID-A
// departure after bounded gameplay, and then requests its own clean leave.

#include <BWAPI.h>

#include <cstdio>
#include <string>

#ifndef VOID_OPENBW_SMOKE_ROLE
#error "VOID_OPENBW_SMOKE_ROLE must be defined as 0 or 1"
#endif
#if VOID_OPENBW_SMOKE_ROLE != 0 && VOID_OPENBW_SMOKE_ROLE != 1
#error "VOID_OPENBW_SMOKE_ROLE must be defined as 0 or 1"
#endif

namespace {

constexpr int kBoundedLeaveFrame = 480;
constexpr int kNamedPeerDepartureMinFrame = 360;

const char* role_name() {
#if VOID_OPENBW_SMOKE_ROLE == 0
  return "A";
#else
  return "B";
#endif
}

const char* expected_peer_name() {
#if VOID_OPENBW_SMOKE_ROLE == 0
  return "VOID-B";
#else
  return "VOID-A";
#endif
}

class VoidWarCollegeOpenBWSmokeBot final : public BWAPI::AIModule {
 public:
  void onStart() override {
    BWAPI::Broodwar->setCommandOptimizationLevel(0);
    const bool self_present = BWAPI::Broodwar->self() != nullptr;
    const bool enemy_present = BWAPI::Broodwar->enemy() != nullptr;
    const std::string map_name = BWAPI::Broodwar->mapFileName();

    std::printf("bot_role=%s\n", role_name());
    std::printf("bot_on_start=true\n");
    std::printf("bot_start_frame=%d\n", BWAPI::Broodwar->getFrameCount());
    std::printf("bot_multiplayer=%s\n",
                BWAPI::Broodwar->isMultiplayer() ? "true" : "false");
    std::printf("bot_self_present=%s\n", self_present ? "true" : "false");
    std::printf("bot_enemy_present=%s\n", enemy_present ? "true" : "false");
    std::printf("bot_complete_map_information_enabled=%s\n",
                BWAPI::Broodwar->isFlagEnabled(
                    BWAPI::Flag::CompleteMapInformation) ? "true" : "false");
    std::printf("bot_user_input_enabled=%s\n",
                BWAPI::Broodwar->isFlagEnabled(
                    BWAPI::Flag::UserInput) ? "true" : "false");
    std::printf("bot_map_file=%s\n", map_name.c_str());
    if (BWAPI::Broodwar->self()) {
      std::printf("bot_self_name=%s\n", BWAPI::Broodwar->self()->getName().c_str());
    }
    if (BWAPI::Broodwar->enemy()) {
      std::printf("bot_enemy_name=%s\n", BWAPI::Broodwar->enemy()->getName().c_str());
    }
    std::fflush(stdout);
  }

  void onFrame() override {
    const int frame = BWAPI::Broodwar->getFrameCount();
    if (frame == 120 || frame == 240 || frame == 360) {
      std::printf("bot_frame_%d=true\n", frame);
      std::fflush(stdout);
    }

#if VOID_OPENBW_SMOKE_ROLE == 0
    if (!leave_requested_ && frame >= kBoundedLeaveFrame) {
      leave_requested_ = true;
      std::printf("bounded_leave_requested=true\n");
      std::printf("bot_leave_requested_frame=%d\n", frame);
      std::fflush(stdout);
      BWAPI::Broodwar->leaveGame();
    }
#else
    if (!leave_requested_ && named_peer_departure_observed_) {
      leave_requested_ = true;
      std::printf("bounded_peer_followup_leave_requested=true\n");
      std::printf("bot_leave_requested_frame=%d\n", frame);
      std::fflush(stdout);
      BWAPI::Broodwar->leaveGame();
    }
#endif
  }

  void onPlayerLeft(BWAPI::Player player) override {
    const int frame = BWAPI::Broodwar->getFrameCount();
    std::string peer_name;
    if (player) peer_name = player->getName();

    std::printf("bot_peer_left=true\n");
    std::printf("bot_peer_left_frame=%d\n", frame);
    std::printf("bot_peer_left_name=%s\n", peer_name.c_str());

    if (!named_peer_departure_observed_ &&
        frame >= kNamedPeerDepartureMinFrame &&
        peer_name == expected_peer_name()) {
      named_peer_departure_observed_ = true;
      std::printf("bot_named_peer_departure=true\n");
      std::printf("bot_named_peer_departure_frame=%d\n", frame);
      std::printf("bot_named_peer_departure_name=%s\n", peer_name.c_str());
    }
    std::fflush(stdout);
  }

  void onEnd(bool is_winner) override {
    std::printf("bot_on_end=true\n");
    std::printf("bot_end_winner=%s\n", is_winner ? "true" : "false");
    std::printf("bot_end_frame=%d\n", BWAPI::Broodwar->getFrameCount());
    std::fflush(stdout);
  }

 private:
  bool leave_requested_ = false;
  bool named_peer_departure_observed_ = false;
};

}  // namespace

extern "C" void gameInit(BWAPI::Game* game) {
  BWAPI::BroodwarPtr = game;
  std::printf("bot_game_init=true\n");
  std::fflush(stdout);
}

extern "C" BWAPI::AIModule* newAIModule() {
  std::printf("bot_new_ai_module=true\n");
  std::fflush(stdout);
  return new VoidWarCollegeOpenBWSmokeBot();
}
