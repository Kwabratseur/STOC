#test_sample.py
from obscuresecure.main import *


def test_encryption():
  test = "testie"
  Tofile(test)
  assert(Fromfile()) == test

def test_primes():
    assert(isPrime(3)) == True
    assert(isPrime(13)) == True
    assert(isPrime(6)) == False
