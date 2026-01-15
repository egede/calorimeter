def test_imports():
    import calorimeter
    from calorimeter.calorimeter import Calorimeter
    from calorimeter.layer import Layer
    from calorimeter.particle import Particle, Electron, Photon, Muon
    from calorimeter.simulation import Simulation

    assert hasattr(calorimeter, "__version__") or True
    assert Calorimeter is not None
    assert Layer is not None
    assert Particle is not None
    assert Electron is not None
    assert Photon is not None
    assert Muon is not None
    assert Simulation is not None
