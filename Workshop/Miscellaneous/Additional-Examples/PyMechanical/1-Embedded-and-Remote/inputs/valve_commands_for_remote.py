import os

inputs_dir = os.path.join(os.getcwd(),"inputs")
geom_file_name = "Valve_Geometry_NS.scdoc"
mat_file_name = "MatML2.xml"
mechdat_file_name = "embedded_nb_200.mechdb"
mat_file_name = "MatML2.xml"
mechdat_file_name = "embedded_nb_200.mechdb"

outputs_dir = os.path.join(os.getcwd(),"outputs")
work_dir = os.path.join(os.getcwd(),"wdir")


#Geometry file with Named Selections Defined
geometryfilewithpath = os.path.join(inputs_dir,geom_file_name )

#Materials file (Select Multiple Materials in Engg Data > Export)
matfilewithpath = os.path.join(inputs_dir, mat_file_name)

# File name to save (Standalone Mechanical uses Mechdb and Mechdat)
mechdat_filepath = os.path.join(work_dir, mechdat_file_name) # edit this filename



"""Import board geometry with specified settings"""
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = (Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic)
geometry_import_preferences = (Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences())
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(geometryfilewithpath, geometry_import_format, geometry_import_preferences)

"""Import Materials from xml file created from Engineering Data"""
Model.Materials.Import(matfilewithpath)
ExtAPI.DataModel.Project.Save(mechdat_filepath)

# Define mesh settings
mesh = Model.Mesh
mesh.ElementSize = Quantity('25 [mm]')
mesh.GenerateMesh()


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



# Solve model
analysis.Solve()




# Add results
solution = analysis.Solution
solution.AddTotalDeformation()
solution.AddEquivalentStress()
solution.EvaluateAllResults()

# Export result values to a text file
results =  solution.GetChildren(DataModelObjectCategory.Result,True)
for result in results:
    fileName = str(result.Name)
    path = os.path.join(outputs_dir,fileName + "_remote"+r".txt")
    result.ExportToTextFile(True,path)

ExtAPI.DataModel.Project.Save(mechdat_filepath)