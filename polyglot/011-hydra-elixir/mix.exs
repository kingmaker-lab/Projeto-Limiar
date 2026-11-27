defmodule Hydra.MixProject do
  use Mix.Project

  def project, do: [app: :hydra, version: "0.1.0", elixir: "~> 1.14", escript: [main_module: Hydra.CLI, path: ".build/hydra"]]
  def application, do: [mod: {Hydra.Application, []}]
end
