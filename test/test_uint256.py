import pytest

from paml.uint256 import *

@pytest.fixture
def tA():
    # Each row must be a maximum of 16 hex characters (64-bits)
    return (0x7000000000000000,  # High
            0x0000000000000000,  # Mid2
            0x0000000000000000,  # Mid1
            0x0000000000000002)  # Low


@pytest.fixture
def tB():
    return (0x7000000000000000,
            0x0000000000000000,
            0x0000000000000000,
            0x0000000000000000)

@pytest.fixture
def tC():
    return (0x7000000000000000,
            0x0000000000000000,
            0x0000000000000000,
            0x0000000000000004)

@pytest.fixture
def tD():
    return (0x9000000000000000,
            0x0000000000000000,
            0x0000000000000000,
            0x0000000000000000)

@pytest.fixture
def tE():
    return (0xE000000000000000,
            0x0000000000000000,
            0x0000000000000000,
            0x0000000000000006)

def test_uint256_cmp(tA, tB, tC):

    intA = uint256(*tA)
    assert intA is not None, "Creating intA result in None"

    intB = uint256(*tB)
    assert intB is not None, "Creating intB result in None"

    intC = uint256(*tC)
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

def test_uint256_get(tA, tB, tC):

    intA = uint256(*tA)
    assert intA is not None, "Creating intA result in None"

    intB = uint256(*tB)
    assert intB is not None, "Creating intB result in None"

    intC = uint256(*tC)
    assert intC is not None, "Creating intC result in None"

    # #########
    # Get Value
    # #########

    assert tA == intA.get(), "tA != intA.get()"
    assert tB == intB.get(), "tB !=  intB.get()"
    assert tC == intC.get(), "tC !=  intC.get()"

def test_uint256_add(tA, tC, tD, tE):

    intA = uint256(*tA)
    assert intA is not None, "Creating intA result in None"

    intC = uint256(*tC)
    assert intC is not None, "Creating intC result in None"

    intD = uint256(*tD)
    assert intD is not None, "Creating intD result in None"

    intE = uint256(*tE)
    assert intD is not None, "Creating intD result in None"

    intAC = intA + intC
    assert intAC == intE
    with pytest.raises(uint256OverflowError): 
        intAD, o = intA.add(intD)
        assert intAD == None, "intA + intD did NOT Overflow!"
        raise o
