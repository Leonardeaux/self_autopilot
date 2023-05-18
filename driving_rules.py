from game_events import straight_event, right_event, left_event, backward_event


def not_really_an_ai(lane_slope_1: float, lane_slope_2: float) -> None:
    if lane_slope_1 < 0 and lane_slope_2 < 0:
        right_event()
    elif lane_slope_1 > 0 and lane_slope_2 > 0:
        left_event()
    else:
        straight_event()