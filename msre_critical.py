import openmc
import openmc.deplete
import openmc.lib
import numpy as np
from math import log10
import math
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
from openmc.mpi import comm

import os
salt_temp = float(os.environ.get('SALT_TEMP', 648.9))
salt = openmc.Material(name="salt", temperature = salt_temp + 273.15)
salt.add_nuclide('Li6', 0.000013154112468023)
salt.add_nuclide('Li7', 0.26308224936046)
salt.add_nuclide('Be9', 0.118688701012415)
salt.add_nuclide('Zr90', 0.0105474635407522)
salt.add_nuclide('Zr91', 0.00230014656807074)
salt.add_nuclide('Zr92', 0.00351582118025073)
salt.add_nuclide('Zr94', 0.00356297213485467)
salt.add_nuclide('Zr96', 0.000574011621265425)
salt.add_nuclide('Hf174', 8.38247740140624E-10)
salt.add_nuclide('Hf176', 2.7557394457123E-08)
salt.add_nuclide('Hf177', 9.74462997913475E-08)
salt.add_nuclide('Hf178', 1.42921239693976E-07)
salt.add_nuclide('Hf179', 7.13558388794706E-08)
salt.add_nuclide('Hf180', 1.83785817025832E-07)
salt.add_nuclide('U234', 1.0347565262903E-05)
salt.add_nuclide('U235', 0.00101016468225742)
salt.add_nuclide('U236', 4.22977313470575E-06)
salt.add_nuclide('U238', 0.00216927468770906)
salt.add_nuclide('Fe54', 2.85638006498257E-06)
salt.add_nuclide('Fe56', 4.48390584229958E-05)
salt.add_nuclide('Fe57', 1.03552940251464E-06)
salt.add_nuclide('Fe58', 1.37809953520117E-07)
salt.add_nuclide('Cr50', 2.12334839732237E-06)
salt.add_nuclide('Cr52', 4.09466602677201E-05)
salt.add_nuclide('Cr53', 4.64302258295968E-06)
salt.add_nuclide('Cr54', 1.15574659601091E-06)
salt.add_nuclide('Ni58', 5.86242346937877E-06)
salt.add_nuclide('Ni60', 2.25819502474211E-06)
salt.add_nuclide('Ni61', 9.8162174140492E-08)
salt.add_nuclide('Ni62', 3.1298396518433E-07)
salt.add_nuclide('Ni64', 7.97077887397486E-08)
salt.add_nuclide('O16', 5.14608150091125E-05)
salt.add_nuclide('O17', 1.89357307228381E-08)
salt.add_nuclide('O18', 9.64845134923903E-08)
salt.add_nuclide('F19', 0.594362994831631)
salt_density = 2.848 - 7.693e-4 * salt_temp   # ORNL-3913 correlation
salt.set_density('g/cm3', salt_density)
salt.volume = (4560*1000)/salt_density

graphite = openmc.Material(name='graphite',temperature= salt_temp + 273.15)
graphite.set_density('g/cm3',1.86)
graphite.add_nuclide('C12',1)
graphite.add_s_alpha_beta('c_Graphite')

inor = openmc.Material(name='inor-8',temperature= salt_temp + 273.15)
inor.set_density('g/cm3',8.7745)
inor.add_element('Ni',(66+71)/2,'wo')
inor.add_element('Mo',(15+18)/2,'wo')
inor.add_element('Cr',(6+8)/2,'wo')
inor.add_element('Fe',5,'wo')
inor.add_element('C',(0.04+0.08)/2,'wo')
inor.add_element('Al',0.25,'wo')
inor.add_element('Ti',0.25,'wo')
inor.add_element('S',0.02,'wo')
inor.add_element('Mn',1.0,'wo')
inor.add_element('Si',1.0,'wo')
inor.add_element('Cu',0.35,'wo')
inor.add_element('B',0.010,'wo')
inor.add_element('W',0.5,'wo')
inor.add_element('P',0.015,'wo')
inor.add_element('Co',0.2,'wo')

helium = openmc.Material(name='helium')
helium.add_element('He',1.0)
helium.set_density('g/cm3',1.03*(10**-4))

trace = 0.01
inconel = openmc.Material(name='inconel-600', temperature = 65.6 + 273.15)
inconel.add_element('Ni',78.5,percent_type='wo')
inconel.add_element('Cr',14.0,percent_type='wo')
inconel.add_element('Fe',6.5,percent_type='wo')
inconel.add_element('Mn',0.25,percent_type='wo')
inconel.add_element('Si',0.25,percent_type='wo')
inconel.add_element('Cu',0.2,percent_type='wo')
inconel.add_element('Co',0.2,percent_type='wo')
inconel.add_element('Al',0.2,percent_type='wo')
inconel.add_element('Ti',0.2,percent_type='wo')
inconel.add_element('Ta',0.5,percent_type='wo')
inconel.add_element('W',0.5,percent_type='wo')
inconel.add_element('Zn',0.2,percent_type='wo')
inconel.add_element('Zr',0.1,percent_type='wo')
inconel.add_element('C',trace,percent_type='wo')
inconel.add_element('Mo',trace,percent_type='wo')
inconel.add_element('Ag',trace,percent_type='wo')
inconel.add_element('B',trace,percent_type='wo')
inconel.add_element('Ba',trace,percent_type='wo')
inconel.add_element('Be',trace,percent_type='wo')
inconel.add_element('Ca',trace,percent_type='wo')
inconel.add_element('Cd',trace,percent_type='wo')
inconel.add_element('V',trace,percent_type='wo')
inconel.add_element('Sn',trace,percent_type='wo')
inconel.add_element('Mg',trace,percent_type='wo')
inconel.set_density('g/cm3',8.5)

ss316 = openmc.Material(name='ss316', temperature = 65.6 + 273.15)
ss316.add_element('C',0.026,'wo')
ss316.add_element('Si',0.37,'wo')
ss316.add_element('Mn',0.16,'wo')
ss316.add_element('Cr',16.55,'wo')
ss316.add_element('Cu',0.16,'wo')
ss316.add_element('Ni',10,'wo')
ss316.add_element('P',0.029,'wo')
ss316.add_element('S',0.027,'wo')
ss316.add_element('Mo',2.02,'wo')
ss316.add_element('N',0.036,'wo')
ss316.add_element('Fe',70.622,'wo')
ss316.set_density('g/cm3',7.99)

Gd2O3 = openmc.Material()
Gd2O3.add_element('Gd',2)
Gd2O3.add_element('O',3)
Gd2O3.set_density('g/cm3',7.41)
Al2O3 = openmc.Material()
Al2O3.add_element('Al',2)
Al2O3.add_element('O',3)
Al2O3.set_density('g/cm3',3.95)
bush = openmc.Material.mix_materials([Gd2O3,Al2O3],[0.7,0.3],'wo')
bush.name='Gd2O3-Al2O3'
bush.temperature = 65.6 +273.15

concrete = openmc.Material(name='concrete')
concrete.add_element('H',0.005,'wo')
concrete.add_element('O',0.496,'wo')
concrete.add_element('Si',0.314,'wo')
concrete.add_element('Ca',0.083,'wo')
concrete.add_element('Na',0.017,'wo')
concrete.add_element('Mn',0.002,'wo')
concrete.add_element('Al',0.046,'wo')
concrete.add_element('S',0.001,'wo')
concrete.add_element('K',0.019,'wo')
concrete.add_element('Fe',0.012,'wo')
concrete.set_density('g/cm3',2.35)

water = openmc.Material()
water.add_element('H',2)
water.add_element('O',1)
water.set_density('g/cm3',0.997)

ss304 =  openmc.Material()
ss304.add_element('C',0.08,'wo')
ss304.add_element('Mn',2,'wo')
ss304.add_element('P',0.045,'wo')
ss304.add_element('S',0.03,'wo')
ss304.add_element('Si',0.75,'wo')
ss304.add_element('Cr',19,'wo')
ss304.add_element('Ni',10,'wo')
ss304.add_element('N',0.1,'wo')
ss304.add_element('Fe',67.995, 'wo')
ss304.set_density('g/cm3',7.93)
shield = openmc.Material.mix_materials([water,ss304],[0.5,0.5],'vo')
shield.temperature = 32.2 + 273.15
shield.name='steelwater'

insulation=openmc.Material(name='insulation')
insulation.add_element('Si',1)
insulation.add_element('O',2)
insulation.set_density('g/cm3',0.16)

watersand=openmc.Material(name='watersand')
watersand.add_element('Fe',3)
watersand.add_element('O',4)
watersand.set_density('g/cm3',6)

steel = openmc.Material(name='steel')
steel.add_element('Fe',1)
steel.set_density('g/cm3',7.85)

mats = openmc.Materials([salt, graphite, inor, helium, inconel, shield, concrete,
                         steel, ss316, watersand, insulation, bush])

# CAD h5m files
core_h5m = 'msre_core.h5m'
pit_h5m = 'msre_pit.h5m'
control_rod1_h5m = 'msre_control_rod.h5m'

#Geometry
core_univ = openmc.DAGMCUniverse(filename = core_h5m, auto_geom_ids = True,
                            universe_id = 1)
pit_univ = openmc.DAGMCUniverse(filename = pit_h5m, auto_geom_ids = True,
                            universe_id = 3) # <-- ADDED THIS
control_rod1 = openmc.DAGMCUniverse(filename = control_rod1_h5m,
                            auto_geom_ids = True, universe_id=2)

core_region = core_univ.bounding_region()
pit_region = pit_univ.bounding_region(starting_id=30000) # <-- ADDED THIS

# Extend control rod region1 to include upwards translations
cr0_region = control_rod1.bounding_region(boundary_type='transmission', starting_id=20000)
cr0_region = cr0_region | cr0_region.translate([0, 0, 150])

# Shift control rods 1 by offset to defined control rod 2 and 3 regions
offset = 10.163255 #cm, offset between cr1, cr2 and cr3
cr1_region = cr0_region.translate([-offset*0.5, -offset*0.5, 0])
cr2_region = cr0_region.translate([ offset*0.5, -offset*0.5, 0])
cr3_region = cr0_region.translate([ offset*0.5,  offset*0.5, 0])
#Define cells
# The pit cell fills the pit region, *except* for the core and control rods
pit_cell = openmc.Cell(region=~(cr1_region | cr2_region | cr3_region | core_region) & pit_region,
                      fill=pit_univ)

# The core cell fills the core region, *except* for the control rods
core_cell = openmc.Cell(region=~(cr1_region | cr2_region | cr3_region) & core_region ,
                        fill=core_univ)
cr1_cell = openmc.Cell(name='CR1', region=cr1_region, fill=control_rod1)

cr2_cell = openmc.Cell(name='CR2', region=cr2_region, fill=control_rod1)
cr3_cell = openmc.Cell(name='CR3', region=cr3_region, fill=control_rod1)

#Fix control rods initial positions
start_pos = 19.2 #cm, geometrical distance between lower bottom and starting point
top_pos = 51 * 2.54 # cm, initial position of control rod1 with respect to start post
init_pos = 16 * 2.54
setattr(cr1_cell, 'translation', [-offset*0.5, -offset*0.5, start_pos + top_pos])
setattr(cr2_cell, 'translation', [ offset*0.5,-offset*0.5, start_pos + top_pos])
setattr(cr3_cell, 'translation', [ offset*0.5,  offset*0.5, start_pos + top_pos])
geometry = openmc.Geometry([pit_cell, core_cell,cr1_cell,cr2_cell,cr3_cell])

# Settings
settings = openmc.Settings()
settings.temperature = {'method':'interpolation','range':(293.15,1300.0)}
settings.batches = 50
settings.inactive = 10
settings.particles = 10000
settings.photon_transport = False
source_area = openmc.stats.Box([-100., -100., 0.],[ 100.,  100.,  200.],
              only_fissionable = True)
settings.source = openmc.Source(space = source_area)

#Tallies
tally = OrderedDict()
tally['general'] = openmc.Tally(name="General")
if settings.photon_transport:
    heating_score = 'heating'
else:
    heating_score = 'heating-local'
tally['general'].scores.append(heating_score)

e_min, e_max = 1e-5, 20e6
groups = 256
energies = np.logspace(log10(e_min), log10(e_max), groups + 1)
energy_filter = openmc.EnergyFilter(energies)
particle_filter = openmc.ParticleFilter(['neutron'])
cell_filter = openmc.MaterialFilter([salt])
tally['flux']= openmc.Tally(name="flux")
tally['flux'].filters = [energy_filter, particle_filter, cell_filter]
tally['flux'].scores = ['flux']
tallies = openmc.Tallies(tally.values())

# Depletion settings
model = openmc.model.Model(geometry,mats,settings,tallies)

#Plots
colors = {salt:'yellow', graphite:'black', inor: 'grey', helium: 'cyan', inconel: 'grey',
              bush: 'blue', ss316: 'grey', concrete: 'brown', shield: 'red', insulation: 'green',
              watersand: 'lightgreen', steel: 'grey'}
plots = openmc.Plots()
plot = openmc.Plot()
plot.basis = 'xy'
plot.width = (150,150)
plot.pixels = (1500,1500)
plot.origin = (0,0,160)
plot.color_by = 'material'
plot.colors = colors
model.plots.append(plot)
plot = openmc.Plot()
plot.basis = 'xz'
plot.width = (150,300)
plot.pixels = (750,1500)
plot.origin = (0,-5,150)
plot.color_by = 'material'
plot.colors = colors
model.plots.append(plot)
plot = openmc.Plot()
plot.basis = 'yz'
plot.width = (150,300)
plot.pixels = (500,1000)
plot.origin = (5,0,150)
plot.color_by = 'material'
plot.colors = colors
model.plots.append(plot)

if comm.rank == 0:
    model.export_to_xml()
comm.barrier()
openmc.lib.init(intracomm=comm)
openmc.lib.run(output=True)
comm.barrier()
openmc.lib.finalize()
