import pytest
import numbers
from world_bank_data import get_indicators, get_series
from .tools import assert_numeric_or_string


def test_indicators_one():
    idx = get_indicators('SP.POP.TOTL')
    assert idx.index == ['SP.POP.TOTL']
    assert_numeric_or_string(idx)


def test_indicators_two():
    with pytest.raises(RuntimeError):
        get_indicators(['SP.POP.0014.TO.ZS', 'SP.POP.TOTL'])


def test_indicators():
    idx = get_indicators()
    assert len(idx.index) > 16000
    assert_numeric_or_string(idx)


def test_indicators_topic():
    idx = get_indicators(topic=5)
    assert len(idx.index) < 100
    assert_numeric_or_string(idx)


def test_indicator_most_recent_value():
    idx = get_series('SP.POP.TOTL', mrv=1)
    assert len(idx.index) > 200
    assert_numeric_or_string(idx)

    idx_mrv5 = get_series('SP.POP.TOTL', mrv=5)
    assert len(idx_mrv5.index) == 5 * len(idx.index)
    assert_numeric_or_string(idx_mrv5)


def test_indicator_use_id():
    idx = get_series('SP.POP.TOTL', mrv=1, id_or_value='id', simplify_index=True)
    assert len(idx.index) > 200
    assert_numeric_or_string(idx)
    assert idx.name == 'SP.POP.TOTL'
    assert idx.index.names == ['Country']


def test_indicator_simplify_scalar():
    pop = get_series('SP.POP.TOTL', 'CHN', mrv=1, simplify_index=True)
    assert isinstance(pop, numbers.Number)


def test_indicator_date():
    idx = get_series('SP.POP.TOTL', date='2010:2018')
    assert len(idx.index) > 200 * 8
    assert_numeric_or_string(idx)


@pytest.mark.skip('jsonstat format not supported here')
def test_indicator_monthly():
    idx = get_series('DPANUSSPB', country=['CHN', 'BRA'], date='2012M01:2012M08')
    assert len(idx.index) > 200 * 12
    assert_numeric_or_string(idx)
