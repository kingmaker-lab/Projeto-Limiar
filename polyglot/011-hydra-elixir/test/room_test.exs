defmodule Hydra.RoomTest do
  use ExUnit.Case

  test "subscriptions survive dispatcher restart" do
    assert {:ok, _} = Hydra.Room.subscribe("ops")
    assert :ok = Hydra.Room.publish("other", "ignored")
    refute_received {:hydra, _, _}
    assert :ok = Hydra.Room.publish("ops", "before")
    assert_receive {:hydra, "ops", "before"}
    assert :ok = Supervisor.terminate_child(Hydra.Supervisor, Hydra.Room)
    assert {:error, :unavailable} = Hydra.Room.publish("ops", "offline")
    assert {:ok, _} = Supervisor.restart_child(Hydra.Supervisor, Hydra.Room)
    assert :ok = Hydra.Room.publish("ops", "after")
    assert_receive {:hydra, "ops", "after"}
    assert {:error, :invalid_message} = Hydra.Room.publish("ops", "")
  end
end
