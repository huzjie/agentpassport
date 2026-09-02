# -*- coding: utf-8 -*-
from agentpassport.channel import ChannelMonitor, TopologyPolicy
from agentpassport.errors import UnauthorizedChannelError


def test_unauthorized_channel():
    mon = ChannelMonitor(TopologyPolicy())
    import pytest
    with pytest.raises(UnauthorizedChannelError):
        mon.record("a", "b", "secret", authorized=False)


def test_topology_hub():
    mon = ChannelMonitor(TopologyPolicy())
    mon.record("hub", "a", "c", authorized=True)
    mon.record("hub", "b", "c", authorized=True)
    mon.record("hub", "c", "c", authorized=True)
    assert mon.current_topology() == "hub"
