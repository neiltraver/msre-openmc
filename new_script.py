import CAD_to_OpenMC.assembly as ab

CORE = ab.Assembly(stp_files=['msre_core.step'])
CORE.run(backend='stl2', merge=True, h5m_file='msre_core.h5m')

PIT = ab.Assembly(stp_files=['msre_pit.step'])
PIT.run(backend='stl2', merge=True, h5m_file='msre_pit.h5m')

CR = ab.Assembly(stp_files=['msre_control_rod.step'])
CR.run(backend='stl2', merge=True, h5m_file='msre_control_rod.h5m')

