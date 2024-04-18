### Imports

import os
from ansys.mechanical.core import embedding as app
from ansys.mechanical.core import global_variables

### Input Parameters : Folders . Ansys Version

inputs_dir = os.path.join(os.getcwd(),"inputs")
geom_file_name = "Valve_Geometry_NS.scdoc"
mat_file_name = "MatML2.xml"
mechdat_file_name = "embedded_205.mechdb"

outputs_dir = os.path.join(os.getcwd(),"outputs")
work_dir = os.path.join(os.getcwd(),"wdir")

ansys_version = 241

### Construct Absolute File paths
[os.makedirs(folder) for folder in ('wdir', 'outputs') if not os.path.exists(folder)]

#Geometry file with Named Selections Defined
geometryfilewithpath = os.path.join(inputs_dir,geom_file_name )

#Materials file (Select Multiple Materials in Engg Data > Export)
matfilewithpath = os.path.join(inputs_dir, mat_file_name)

# File name to save (Standalone Mechanical uses Mechdb and Mechdat)
mechdat_filepath = os.path.join(work_dir, mechdat_file_name) # edit this filename


### Create an Embedded Instance of Mechanical
e_app = app.App(version=ansys_version)
print(e_app)
globals().update(global_variables(e_app, True))


### Import Geometry and Materials
"""Import board geometry with specified settings"""
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = (Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic)
geometry_import_preferences = (Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences())
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(geometryfilewithpath, geometry_import_format, geometry_import_preferences)

"""Import Materials from xml file created from Engineering Data"""
Model.Materials.Import(matfilewithpath)
e_app.save(mechdat_filepath)

### Verify : Count of Bodies and Names of Materials


allbodies=ExtAPI.DataModel.Project.Model.GetChildren( Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body,True)
print("\nTotal Number of Bodies : ", allbodies.Count)

print("Materials available : ")
for mat in Model.Materials.Children:
    print(mat.Name)


### Assign a different material to a body
part =  ExtAPI.DataModel.GetObjectsByName("Connector")[0]
part.Material = "Gray Cast Iron"
ExtAPI.DataModel.Tree.Refresh()

e_app.save(mechdat_filepath)

### Assign Mesh Settings. Generate Mesh
# Define mesh settings
mesh = Model.Mesh
mesh.ElementSize = Quantity('25 [mm]')
mesh.GenerateMesh()

### Assign Loads and Boundary Conditions 


# Define boundary conditions:
analysis = Model.AddStaticStructuralAnalysis()

fixedSupport = analysis.AddFixedSupport()
fixedSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFixedSupportFaces")[0]

frictionlessSupport = analysis.AddFrictionlessSupport()
frictionlessSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFrictionlessSupportFaces")[0]

pressure = analysis.AddPressure()
pressure.Location = ExtAPI.DataModel.GetObjectsByName("NSInsideFaces")[0]
pressure.Magnitude.Inputs[0].DiscreteValues = [Quantity("0 [s]"), Quantity("1 [s]")]
pressure.Magnitude.Output.DiscreteValues = [Quantity("0 [Pa]"), Quantity("15 [MPa]")]

e_app.save(mechdat_filepath)


### Solve and Save

# Solve model
analysis.Solve()

e_app.save(mechdat_filepath)


### Add Result Objects . Evaluate . Export Results as a text file .


# Add results
solution = analysis.Solution
solution.AddTotalDeformation()
solution.AddEquivalentStress()
solution.EvaluateAllResults()
e_app.save(mechdat_filepath)

# Export result values to a text file
results =  solution.GetChildren(DataModelObjectCategory.Result,True)
for result in results:
    fileName = str(result.Name)
    path = os.path.join(outputs_dir,fileName+r".txt")
    result.ExportToTextFile(True,path)



### Close the Embedded Instance
e_app.close()







