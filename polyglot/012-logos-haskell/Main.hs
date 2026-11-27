module Main where
import Logos
import System.Environment (getArgs)
import System.Exit (die)

main :: IO ()
main = do
  args <- getArgs
  case args of
    ["eval", expr] -> either die print (evaluate [] expr)
    ["rule", op, expr] -> either die print (checkRule [] op expr)
    _ -> die "usage: logos eval EXPR | logos rule OP 'LHS;RHS'"
