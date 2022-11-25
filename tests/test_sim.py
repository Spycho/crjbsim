from src.simulation import sim


def test_sim():
    test_list = []
    sim.run_sim(lambda: test_list.append(1))
    assert test_list == [1]


def test_sim_post_process():
    test_list = []
    sim.run_sim(lambda: test_list.append(1), lambda: test_list.append(2))
    assert test_list == [1, 2]
