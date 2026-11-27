defmodule Hydra.Application do
  use Application

  def start(_type, _args) do
    Supervisor.start_link(
      [{Registry, keys: :duplicate, name: Hydra.Registry}, Hydra.Room],
      strategy: :rest_for_one, name: Hydra.Supervisor
    )
  end
end

defmodule Hydra.Room do
  use GenServer

  def start_link(_), do: GenServer.start_link(__MODULE__, nil, name: __MODULE__)

  def subscribe(room) do
    if valid_room?(room), do: Registry.register(Hydra.Registry, room, nil), else: {:error, :invalid_room}
  end

  def publish(room, message) do
    if valid_room?(room) and is_binary(message) and byte_size(message) in 1..4096 and String.valid?(message) do
      try do
        GenServer.call(__MODULE__, {:publish, room, message})
      catch
        :exit, _ -> {:error, :unavailable}
      end
    else
      {:error, :invalid_message}
    end
  end

  defp valid_room?(room), do: is_binary(room) and byte_size(room) <= 32 and Regex.match?(~r/\A[a-z0-9_-]+\z/, room)

  @impl true
  def init(nil), do: {:ok, nil}

  @impl true
  def handle_call({:publish, room, message}, _from, state) do
    Registry.dispatch(Hydra.Registry, room, fn entries ->
      for {pid, _} <- entries, do: send(pid, {:hydra, room, message})
    end)
    {:reply, :ok, state}
  end
end

defmodule Hydra.CLI do
  def main([room]) do
    case Hydra.Room.subscribe(room) do
      {:ok, _} ->
        IO.stream(:stdio, :line)
        |> Enum.each(fn line ->
          case Hydra.Room.publish(room, String.trim_trailing(line, "\n")) do
            :ok ->
              receive do
                {:hydra, ^room, text} -> IO.puts("[#{room}] #{text}")
              after
                1000 -> IO.puts(:stderr, "delivery timeout")
              end
            {:error, reason} -> IO.puts(:stderr, to_string(reason))
          end
        end)
      {:error, _} -> System.halt(2)
    end
  end

  def main(_) do
    IO.puts(:stderr, "usage: hydra ROOM")
    System.halt(2)
  end
end
