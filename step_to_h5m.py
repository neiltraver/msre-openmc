import CAD_to_OpenMC.assembly as ab

for name in ["msre_core", "msre_pit", "msre_control_rod"]:
    a = ab.Assembly()
    a.stp_files = [f"{name}.step"]
    a.import_stp_files()
    a.merge_all()
    a.solids_to_h5m(backend="stl2", h5m_filename=f"{name}.h5m")
