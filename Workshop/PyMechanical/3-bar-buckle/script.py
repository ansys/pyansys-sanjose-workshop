'''

note:
    when running inside mechanical (remote, ansys-mechanical CLI, and paste into script editor), the full path is needed.
    when running with embedding, the full path is not needed.

    when running the remote interface, the print statements are ignored. Instead, the values can be accessed by running
    code like this:

    import ansys.mechanical.core as mech
    mechanical = mech.launch_mechanical(batch=True, loglevel="DEBUG")
    mechanical.run_python_script_from_file("path\\to\\script.py")
    mechanical.run_python_script("buck_deformation_1.LoadMultiplier")
    mechanical.exit()
'''


# embedding import block. If running in IronPython, this will do nothing.
try:
    import ansys.mechanical.core as mech
    app = mech.App(version=241)
    globals().update(mech.global_variables(app, True))
except ImportError as e:
    pass


import os

geometry_file = os.path.abspath(os.path.join(os.getcwd(), "Files", "Eng157.x_t"))
if not os.path.isfile(geometry_file):
    geometry_file = r"C:\AnsysDev\code\pyansys\Demo_Examples\Workshop\PyMechanical\3-bar-buckle\Files\Eng157.x_t"

geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import.Import(geometry_file)

Model.Geometry.ElementControl = ElementControl.Manual

struc = Model.AddStaticStructuralAnalysis()
buck = Model.AddEigenvalueBucklingAnalysis()
Model.Analyses[1].InitialConditions[0].PreStressICEnvironment = Model.Analyses[0]
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardBIN

ns_support = Model.AddNamedSelection()
ns_support.ScopingMethod = GeometryDefineByType.Worksheet
ns_support.Name = "NS_SUPPORT"
ns_support.GenerationCriteria.Add()
criteria = ns_support.GenerationCriteria[0]
criteria.EntityType = SelectionType.GeoFace
criteria.Criterion = SelectionCriterionType.LocationZ
criteria.Operator = SelectionOperatorType.Equal
criteria.Value = Quantity('0 [in]')
ns_support.Generate()

fixed_support = struc.AddFixedSupport()
fixed_support.Location = ns_support


ns_force = Model.AddNamedSelection()
ns_force.ScopingMethod = GeometryDefineByType.Worksheet
ns_force.Name = "NS_FORCE"
ns_force.GenerationCriteria.Add()
criteria = ns_force.GenerationCriteria[0]
criteria.EntityType = SelectionType.GeoFace
criteria.Criterion = SelectionCriterionType.LocationZ
criteria.Operator = SelectionOperatorType.Equal
criteria.Value = Quantity('100 [in]')
ns_force.Generate()


force = struc.AddForce()
force.Location = ns_force
force.DefineBy = LoadDefineBy.Components
force.ZComponent.Output.SetDiscreteValue(0, Quantity("-1 [lbf]"))

buck.AnalysisSettings.MaximumModesToFind = 6
buck.AnalysisSettings.Stress = True
buck.AnalysisSettings.Strain = True

buck_deformation_1 = buck.Solution.AddTotalDeformation()
buck_deformation_1.Mode = 1
buck_deformation_2 = buck.Solution.AddTotalDeformation()
buck_deformation_2.Mode = 2
buck_deformation_3 = buck.Solution.AddTotalDeformation()
buck_deformation_3.Mode = 3
buck_deformation_4 = buck.Solution.AddTotalDeformation()
buck_deformation_4.Mode = 4
buck_deformation_5 = buck.Solution.AddTotalDeformation()
buck_deformation_5.Mode = 5
buck_deformation_6 = buck.Solution.AddTotalDeformation()
buck_deformation_6.Mode = 6
buck_stress_eqv = buck.Solution.AddEquivalentStress()
buck_stress_eqv.Mode = 6

Model.Solve(True)
assert buck.Solution.ObjectState == ObjectState.Solved
assert struc.Solution.ObjectState == ObjectState.Solved

print("Mode 1 deformation load multiplier: ", buck_deformation_1.LoadMultiplier)
print("Mode 2 deformation load multiplier: ", buck_deformation_2.LoadMultiplier)
print("Mode 3 deformation load multiplier: ", buck_deformation_3.LoadMultiplier)
print("Mode 4 deformation load multiplier: ", buck_deformation_4.LoadMultiplier)
print("Mode 5 deformation load multiplier: ", buck_deformation_5.LoadMultiplier)
print("Mode 6 deformation load multiplier: ", buck_deformation_6.LoadMultiplier)
print("Mode 6 equivalent stress maximum: ", buck_stress_eqv.Maximum)
