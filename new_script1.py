import CAD_to_OpenMC.assembly as ab

#CORE=ab.Assembly(['msre_core.step'])
#CORE.run(backend='stl2',merge=True,h5m_filename='msre_core.h5m')

#PIT=ab.Assembly(['msre_pit.step'])
#PIT.run(backend='stl2',merge=True,h5m_filename='msre_pit.h5m')

CR=ab.Assembly(['msre_control_rod.step'])
CR.run(backend='stl2',merge=True,h5m_filename='msre_control_rod.h5m')

#ab.merge2h5m([CORE,PIT], h5m_file='msre_reactor.h5m')
