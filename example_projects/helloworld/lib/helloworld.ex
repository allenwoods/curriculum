defmodule HelloWorld do
  @moduledoc """
  Documentation for `HelloWorld`.
  """

  @doc """
  Hello world.

  ## Examples

      iex> assert HelloWorld.hello() |> String.starts_with?("Hello,")

  """
    def hello do
      "Hello, #{Faker.Person.first_name()}."
    end
end
