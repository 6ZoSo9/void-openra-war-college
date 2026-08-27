from tools import conditional_engagement_v2_1_duel_wrapper as wrapper_module


def test_parent_wrapper_error_receives_v21_terminal_hold(monkeypatch, capsys):
    def fail(_argv=None):
        raise wrapper_module.parent.WrapperError("parent loader failed")

    monkeypatch.setattr(wrapper_module, "main", fail)
    assert wrapper_module.cli([]) == 2
    captured = capsys.readouterr()
    assert "VOID_CONDITIONAL_ENGAGEMENT_V2_1_WRAPPER_HOLD" in captured.err
    assert "blocker=parent loader failed" in captured.err
