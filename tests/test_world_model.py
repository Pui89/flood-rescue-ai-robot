from flood_robot.world_model import ObjectClass, ObservationRef, RescueWorldState, WorldObject


def test_world_state_tracks_provenance_and_staleness():
    ref = ObservationRef("rgbd-front", 100, "map", "cal-1", "detector-1")
    obj = WorldObject("victim-1", ObjectClass.PERSON, (1.0, 2.0, 0.5), confidence=0.95)
    obj.observations.append(ref)
    world = RescueWorldState("mission-1", 200, "map", 1)
    world.upsert(obj)
    assert world.get("victim-1") is obj
    assert world.stale_after(50, 200) == ["victim-1"]
