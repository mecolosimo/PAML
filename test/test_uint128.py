import pytest

from paml.uint128 import *

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

def test_uint128_cmp(tA, tB, tC):

    intA = uint128(*tA)
    assert intA is not None, "Creating intA result in None"

    intB = uint128(*tB)
    assert intB is not None, "Creating intB result in None"

    intC = uint128(*tC)
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

def test_uint128_get(tA, tB, tC):

    intA = uint128(*tA)
    assert intA is not None, "Creating intA result in None"

    intB = uint128(*tB)
    assert intB is not None, "Creating intB result in None"

    intC = uint128(*tC)
    assert intC is not None, "Creating intC result in None"

    # #########
    # Get Value
    # #########

    assert tA == intA.get(), "tA != intA.get()"
    assert tB == intB.get(), "tB !=  intB.get()"
    assert tC == intC.get(), "tC !=  intC.get()"

def test_uint128_add(tA, tC, tD, tE):

    intA = uint128(*tA)
    assert intA is not None, "Creating intA result in None"

    intC = uint128(*tC)
    assert intC is not None, "Creating intC result in None"

    intD = uint128(*tD)
    assert intD is not None, "Creating intD result in None"

    intE = uint128(*tE)
    assert intD is not None, "Creating intE result in None"

    intAC = intA + intC
    print(f"\nintAC: {intAC.get()}")
    print(f"intE: {intE.get()}")
    assert intAC == intE, "intA + intC did NOT eq intE!"
    #with pytest.raises(uint128OverflowError): 
    #    intAD, o = intA.add(intD)
    #    assert intAD == None, "intA + intD did NOT Overflow!"
    #    raise o

def test_uint128_subraction(tA, tC, tF):
    
    intA = uint128(*tA)
    assert intA is not None, "Creating intA result in None"

    intC = uint128(*tC)
    assert intC is not None, "Creating intC result in None"

    intF = uint128(*tF)
    assert intF is not None, "Creating intF result in None"

    intCA = intC - intA
    print(f"\nintCA: {intCA.get()}")
    print(f"intF: {intF.get()}")
    #assert intCA == intF, "intC - intA did NOT eq intF"
    #with pytest.raises(uint128UnderflowError): 
    #    intAC, o = intA.sub(intC)
    #    assert intAC == None, "intA + intD did NOT Overflow!"
    #    raise o