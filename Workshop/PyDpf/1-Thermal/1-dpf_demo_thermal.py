from ansys.dpf import core as dpf
from ansys.dpf.core.plotter import DpfPlotter

"""
Load result file and create model database
"""

path = "transient_thermal.rth"

ds = dpf.DataSources(path)
my_model = dpf.Model(ds)
# print(my_model)

my_mesh = my_model.metadata.meshed_region
# print(my_mesh)

"""
Select preferable Named Selection
"""

get_NSs = my_model.metadata.available_named_selections
# print(get_NSs)

my_mesh_scoping = my_model.metadata.named_selection("NODAL_PCB")
# print(my_mesh_scoping)

"""
Scope Named Selection to corresponding Mesh
"""

scoping_op = dpf.operators.mesh.from_scoping()
scoping_op.inputs.scoping.connect(my_mesh_scoping)
scoping_op.inputs.mesh.connect(my_mesh)

my_mesh_ns = scoping_op.outputs.mesh()
# print(my_mesh_ns)

"""
Get Temperature results at last time step
"""

get_all_temps = my_model.results.temperature.on_all_time_freqs
get_fieldContainers_temperature = get_all_temps(mesh_scoping=my_mesh_scoping).eval()

get_field_temperature = get_fieldContainers_temperature[-1]
# print(get_field_temperature)

"""
Contour Plot: Temperature on PCB
"""

my_plot = DpfPlotter()
my_plot.add_field(get_field_temperature, my_mesh_ns)
my_plot.show_figure(show_axes=True)

"""
Min & Max Temperature in the selected field
"""

print("Minimum Temperature: ", round(float(get_field_temperature.data.min()),3), " degC")
print("Maximum Temperature: ", round(float(get_field_temperature.data.max()),3), " degC")
