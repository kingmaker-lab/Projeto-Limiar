module Logos (evaluate, checkRule) where

import Data.Char (isAlpha, isAlphaNum, isAscii, isDigit)
import Data.Ratio ((%))
import Text.ParserCombinators.ReadP

data Expr = Literal Rational | Variable String | Unary Expr | Binary Char Expr Expr

symbol :: String -> ReadP String
symbol token = skipSpaces *> string token

expression :: ReadP Expr
expression = chainl1 term (operator "+-")
  where
    term = chainl1 factor (operator "*/")
    factor = (Unary <$> (symbol "-" *> factor)) <++ atom
    atom = between (symbol "(") (symbol ")") expression <++ (skipSpaces *> (number <++ variable))
    operator chars = do
      skipSpaces
      Binary <$> satisfy (`elem` chars)
    digit = satisfy (\c -> isAscii c && isDigit c)
    number = do
      whole <- munch1 (\c -> isAscii c && isDigit c)
      fraction <- option "" (char '.' *> ((:) <$> digit <*> munch (\c -> isAscii c && isDigit c)))
      return (Literal (read (whole ++ fraction) % (10 ^ length fraction)))
    variable = Variable <$> ((:) <$> satisfy isAlpha <*> munch isAlphaNum)

evaluate :: [(String, Rational)] -> String -> Either String Rational
evaluate bindings input
  | length input > 512 = Left "expression too long"
  | otherwise =
      case [ast | (ast, "") <- readP_to_S (expression <* skipSpaces <* eof) input] of
        [ast] -> run ast
        _ -> Left "invalid expression"
  where
    run (Literal value) = Right value
    run (Variable name) = maybe (Left ("unknown variable: " ++ name)) Right (lookup name bindings)
    run (Unary child) = negate <$> run child
    run (Binary op lhs rhs) = do
      a <- run lhs
      b <- run rhs
      case op of
        '+' -> Right (a + b)
        '-' -> Right (a - b)
        '*' -> Right (a * b)
        '/' | b /= 0 -> Right (a / b)
        _ -> Left "division by zero"

checkRule :: [(String, Rational)] -> String -> String -> Either String Bool
checkRule bindings operator expressionPair =
  case break (== ';') expressionPair of
    (lhs, ';':rhs) -> do
      a <- evaluate bindings lhs
      b <- evaluate bindings rhs
      case operator of
        "<" -> Right (a < b)
        "<=" -> Right (a <= b)
        "==" -> Right (a == b)
        ">=" -> Right (a >= b)
        ">" -> Right (a > b)
        _ -> Left "invalid comparison"
    _ -> Left "expected lhs;rhs"
