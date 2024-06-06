import typing

import ansys.mechanical.core as mech

def _export_image(app: mech.App, output_path: str) -> None:
    """Export the image the given output path."""
    image_settings = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
    image_format = GraphicsImageExportFormat.PNG
    image_settings.Resolution = GraphicsResolutionType.EnhancedResolution
    image_settings.Background = GraphicsBackgroundType.White
    image_settings.CurrentGraphicsDisplay=False
    image_settings.Width = 720
    image_settings.Height = 720
    app.ExtAPI.Graphics.ExportImage(output_path, image_format, image_settings)


def _print_output(app: mech.App, solution_time: float, deformation_max: float, deformation_min: float, deformation_stdev: float) -> None:
    """Print the result output to the console."""
    print("Results:")
    print(f"    Elapsed solution time: {solution_time}s")
    print(f"    Maximum total deformation: {deformation_max}mm")
    print(f"    Minimum total deformation: {deformation_min}mm")
    print(f"    Standard deviation: {deformation_stdev}mm")


def _setup(app: mech.App, velocities: typing.List[float], input_dict: typing.Dict[str, str]):
    """Setup the problem.
    Apply the velocities to the Rotational Velocity object, apply the input_dict to the AUTO_BEARING object.
    """
    # hint: the command to set a row of the rotational velocity Y component table looks like this:
    #           rotational_velocity.YComponent.Output.DiscreteValues[0]=Quantity(1, '[rad/s]')
    bearing = DataModel.GetObjectsByName("AUTO_BEARING")[0]
    bearing.StiffnessK11.Output.SetDiscreteValue(0, Quantity(input_dict["k11"]))
    bearing.StiffnessK22.Output.SetDiscreteValue(0, Quantity(input_dict["k22"]))
    bearing.StiffnessK12.Output.SetDiscreteValue(0, Quantity(input_dict["k12"]))
    bearing.StiffnessK21.Output.SetDiscreteValue(0, Quantity(input_dict["k21"]))
    bearing.DampingC11.Output.SetDiscreteValue(0, Quantity(input_dict["c11"]))
    bearing.DampingC22.Output.SetDiscreteValue(0, Quantity(input_dict["c22"]))
    bearing.DampingC12.Output.SetDiscreteValue(0, Quantity(input_dict["c12"]))
    bearing.DampingC21.Output.SetDiscreteValue(0, Quantity(input_dict["c21"]))

    rotational_velocity = DataModel.GetObjectsByType(DataModelObjectCategory.RotationalVelocity)
    for i in range(len(velocities)):
        rotational_velocity.YComponent.Output.SetDiscreteValue(i, Quantity(velocities[i], "rad/s"))


def _get_output(app) -> typing.Tuple[float, float, float, float]:
    """Get the outputs:
        - Solution time (s)
        - Deformation maximum (mm)
        - Deformation minimum (mm)
        - Deformation standard deviation (mm)
    """
    return 0., 0., 0., 0.


def run(velocities: typing.List[float], mode: int, solve_point: int, model: str, input_dict: typing.Dict[str, str], output: str) -> None:
    """Run the full automation."""
    app=mech.App(version=241)
    assert app.readonly is False, "Mechanical is readonly. Ensure that an appropriate license is available!"
    app.open(model)
    globals().update(mech.global_variables(app, True))

    _setup(app, velocities, input_dict)
    solution_time, deformation_max, deformation_min, deformation_stdev = _get_output(app)

    _print_output(app, solution_time, deformation_max, deformation_min, deformation_stdev)
    _export_image(app, output)
