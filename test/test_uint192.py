import pytest

from paml.uint192 import *
from paml.uint256 import *

@pytest.fixture
def tA():
    return (0x7000000000000000,  # High
            0x0000000000000000,  # Mid
            0x0000000000000002)  # Low


@pytest.fixture
def tB():
    return (0x7000000000000000,
            0x0000000000000000,
            0x0000000000000000)

@pytest.fixture
def tC():
    return (0x7000000000000000,
            0x0000000000000000,
            0x0000000000000004)

@pytest.fixture
def tD():
    return (0x9000000000000000,
            0x0000000000000000,
            0x0000000000000000)

@pytest.fixture
def tE():
    return (0xE000000000000000,
            0x0000000000000000,
            0x0000000000000006)

@pytest.fixture
def tF():
    return (0x0000000000000000,
            0x0000000000000000,
            0x0000000000000002)

@pytest.fixture
def tG():
    return (0x0000000000000000,
            0xE000000000000000,
            0x0000000000000000,
            0x0000000000000000)

def test_uint192_cmp(tA, tB, tC):

    intA = uint192(*tA)
    assert intA is not None, "Creating intA result in None"

    intB = uint192(*tB)
    assert intB is not None, "Creating intB result in None"

    intC = uint192(*tC)
    assert intC is not None, "Creating intC result in None"

    #print(f"\nintA: {intA.get()}\nintB: {intB.get()}", flush=True)

    # ############
    # Comparisions
    # ############

    # intA > entryB
    assert not intA == intB, "intA == entryB!?!"
    assert intA != intB, "intA == entryB!?!"
    assert intA > intB, "intA < entryB!?!"
    assert intA >= intB, "intA < entryB!?!"
    assert not intA < intB, "intA > entryB!?!"
    assert not intA <= intB, "intA > entryB!?!"

    # intC > intA
    assert not intA == intC, "intA == intC!?!"
    assert intA != intC, "intA == intC!?!"
    assert intA < intC, "intA > intC!?!"
    assert intA <= intC, "intA > intC!?!"
    assert not intA > intC, "intA > intC!?!"
    assert not intA >= intC, "intA > intC!?!"
 
    # intC > entryB
    assert not intB == intC, "entryB == intC!?!"
    assert intB != intC, "entryB == intC!?!"
    assert intB < intC, "entryB > intC!?!"
    assert intB <= intC, "entryB > intC!?!"
    assert not intB > intC, "entryB > intC!?!"
    assert not intB >= intC, "entryB > intC!?!"

def test_uint192_get(tA, tB, tC):

    intA = uint192(*tA)
    assert intA is not None, "Creating intA result in None"

    intB = uint192(*tB)
    assert intB is not None, "Creating intB result in None"

    intC = uint192(*tC)
    assert intC is not None, "Creating intC result in None"

    # #########
    # Get Value
    # #########

    assert tA == intA.get(), "tA != intA.get()"
    assert tB == intB.get(), "tB !=  intB.get()"
    assert tC == intC.get(), "tC !=  intC.get()"

def test_uint192_add(tA, tC, tD, tE):

    intA = uint192(*tA)
    assert intA is not None, "Creating intA result in None"

    intC = uint192(*tC)
    assert intC is not None, "Creating intC result in None"

    intD = uint192(*tD)
    assert intD is not None, "Creating intD result in None"

    intE = uint192(*tE)
    assert intD is not None, "Creating intE result in None"

    intAC = intA + intC
    assert intAC == intE, "intA + intC did NOT eq intE!"
    with pytest.raises(uint192OverflowError): 
        intAD, o = intA.add(intD)
        assert intAD == None, "intA + intD did NOT Overflow!"
        raise o

def test_uint192_subraction(tA, tC, tF):
    
    intA = uint192(*tA)
    assert intA is not None, "Creating intA result in None"

    intC = uint192(*tC)
    assert intC is not None, "Creating intC result in None"

    intF = uint192(*tF)
    assert intF is not None, "Creating intF result in None"

    intCA = intC - intA
    assert intCA == intF, "intC - intA did NOT eq intF"
    with pytest.raises(uint192UnderflowError): 
        intAC, o = intA.sub(intC)
        assert intAC == None, "intA + intD did NOT Overflow!"
        raise o
    
def test_uint192_mul(tB, tG):
    
    intB = uint192(*tB)
    assert intB is not None, "Creating intB result in None"

    intG = uint256(*tG)
    assert intG is not None, "Creating intG result in None"

    intB2, _ = intB.mul(2)
    assert intB2 == intG, "intB * 2 is NOT equal to intG"

    intB3, _ = intB.mul(3)
    val = join_uint192(*tB)
    val *= 3            # assume python gives correct answer
    val_parts = split_uint256(val)
    pintB3 = uint256(*val_parts)
    assert intB3 == pintB3, "ARM and Python do NOT Match"

    intB100, _ = intB.mul(100)
    val = join_uint192(*tB)
    val *= 100
    val_parts = split_uint256(val)
    pintB100 = uint256(*val_parts)
    assert intB100 == pintB100, "ARM and Python do NOT Match"