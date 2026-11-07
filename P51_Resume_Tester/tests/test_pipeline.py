import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.design import build_pairs
from src.resumes import render, mask_text
from src.analysis import paired_gap, classify

def test_ten_pairs():
    assert len(build_pairs()) == 10

def test_pairs_differ_only_in_header():
    for p in build_pairs():
        a = render(p.profile_id, p.base_name, p.base_hometown)
        b = render(p.profile_id, p.var_name, p.var_hometown)
        assert mask_text(a, p.base_name, p.base_hometown) == mask_text(b, p.var_name, p.var_hometown)
        assert a != b
        # only one attribute family changes
        if p.attribute == "hometown": assert p.base_name == p.var_name
        else: assert p.base_hometown == p.var_hometown

def test_classify():
    m, lo, hi = paired_gap([70]*5, [66, 66.5, 65.5, 66, 66.2])
    assert classify(m, lo, hi, 3.0) == "FLAG"
    m, lo, hi = paired_gap([70, 71, 69, 70, 70], [70.2, 70.5, 69.6, 70.1, 69.9])
    assert classify(m, lo, hi, 3.0) == "OK"

if __name__ == "__main__":
    test_ten_pairs(); test_pairs_differ_only_in_header(); test_classify(); print("all tests passed")
