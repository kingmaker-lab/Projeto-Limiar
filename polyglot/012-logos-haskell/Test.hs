module Main where
import Control.Monad (unless)
import Logos

main :: IO ()
main = do
  unless (evaluate [("x", 2)] "-x + 3 * 2.5" == Right (11/2)) (fail "precedence")
  unless (evaluate [] "1 / (2-2)" == Left "division by zero") (fail "zero division")
  unless (evaluate [] "1 junk" == Left "invalid expression") (fail "extra token")
  unless (checkRule [] ">=" "1/3;0.3" == Right True) (fail "comparison")
