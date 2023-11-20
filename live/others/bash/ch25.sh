#!/usr/bin/env bash

# Using bash for evaluating math expressions.

function domath() {
  # Doing math using basic bash operators
  declare -i a="$1" b="$2"
  echo "Multiplication: $a * $b = $(($a * $b))"
  echo "Addition:       $a + $b = $(($a + $b))"
  echo "Subtraction:    $a - $b = $(($a - $b))"
  echo "Division:       $a / $b = $(($a / $b))"
  echo "Modulo:         $a % $b = $(($a % $b))"
  echo "Exponentiation: $a ** $b = $(($a ** $b))"
}

function domath_bc() {
  # Doing math using basic bash operators
  declare -i a="$1" b="$2"
  echo "Multiplication: $a * $b = $(bc <<<"$a * $b")"
  echo "Addition:       $a + $b = $(bc <<<"$a + $b")"
  echo "Subtraction:    $a - $b = $(bc <<<"$a - $b")"
  echo "Division:       $a / $b = $(bc -l <<<"$a / $b")"
  echo "Modulo:         $a % $b = $(bc <<<"$a % $b")"
  echo "Exponentiation: $a ^ $b = $(bc <<<"$a ^ $b")"
  # bc can also be used to compare expr
  echo "Equal:          $a == $b = $(bc <<<"$a == $b")"
  echo "NotEqualT:      $a != $b = $(bc <<<"$a != $b")"
  echo "GreaterT:       $a > $b = $(bc <<<"$a >  $b")"
  echo "LessT:          $a < $b = $(bc <<<"$a <  $b")"
  echo "GreaterToE:     $a >= $b = $(bc <<<"$a >= $b")"
  echo "LessToE:        $a <= $b = $(bc <<<"$a <= $b")"
  # Can also support Bool Operations
  echo "And:            $a && $b = $(bc <<<"$a && $b")"
  echo "Or:             $a || $b = $(bc <<<"$a || $b")"
}

function domath_expr() {
  # Note: expr only supports integers
  declare -i a="$1" b="$2"
  echo "Multiplication: $a * $b = $(expr $a \* $b)"
  echo "Addition:       $a + $b = $(expr $a + $b)"
  echo "Subtraction:    $a - $b = $(expr $a - $b)"
  echo "Division:       $a / $b = $(expr $a / $b)"
  echo "Modulo:         $a % $b = $(expr $a % $b)"
}

function bash_arithmetic() {
  # Simple arithmetic with (())
  echo "expression: '6 * 5' | output: $((6 * 5))"
  ((output=3 * 100))
  echo "expression: '3 * 100' | output: $output"
  # Arithmetic command: `let`
  let "number=$output + 300"
  echo "expression: 'number=$output+300' | output: 'number=$number'"
  declare -a vals=(1 2 3 4)
  let "vals[4] = vals[2] + vals[3]"
  echo "Values: ${vals[@]}"
}
