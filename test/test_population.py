import unittest
from geneticAlgo.Population import Population

def f():
	return 4

def test_function():
	assert f() == 4


def test_pop():
	pop = Population()
	assert pop.popSizeToGenerate != None