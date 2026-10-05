from kaykay.core import Gateway,Request
def test_fallback():
    g=Gateway({"bad":lambda r:1/0,"good":lambda r:"ok"},{"m":.001},.01)
    assert g.complete(Request("k","m","hello",1)).provider=="good"
def test_budget():
    g=Gateway({"p":lambda r:"ok"},{"m":1},.001)
    try:g.complete(Request("k","m","hello",100))
    except RuntimeError as e: assert str(e)=="budget_exceeded"
    else: assert False
