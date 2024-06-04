import os
import typing

import ansys.mechanical.core as mech
app=mech.App(version=241)
globals().update(mech.global_variables(app, True))
FILES_PATH = os.path.join(__file__, os.pardir, "Files")

class Problems:
    RIGID_REMOTE_POINT_ON_BEAM_CONNECTION = "A beam connection uses a rigid connection!"
    RIGID_REMOTE_POINT_ON_BEARING = "A bearing uses a rigid connection!"
    WEAK_SPRINGS_ENABLED = "An analysis has weak springs enabled!"

def has_weak_springs():
    def _has_weak_springs(analysis):
        return analysis.AnalysisSettings.WeakSprings == WeakSpringsType.On
    for analysis in app.Model.Analyses:
        if _has_weak_springs(analysis):
            return True
    return False

def has_rigid_beam():
    def _is_rigid(beam):
        if beam.Scope == SpringScopingType.BodyToBody:
            if beam.ReferenceBehavior == LoadBehavior.Rigid:
                return True
        if beam.MobileBehavior == LoadBehavior.Rigid:
            return True
    for beam in app.DataModel.GetObjectsByType(DataModelObjectCategory.Beam):
        if _is_rigid(beam):
            # print(beam.Name + " is rigid")
            return True
    return False

def has_rigid_bearing():
    def _is_rigid(bearing):
        if bearing.ConnectionType == ConnectionScopingType.BodyToBody:
            if bearing.ReferenceBehavior == LoadBehavior.Rigid:
                return True
        if bearing.MobileBehavior == LoadBehavior.Rigid:
            return True
    for bearing in app.DataModel.GetObjectsByType(DataModelObjectCategory.Bearing):
        if _is_rigid(bearing):
            # print(bearing.Name + " is rigid")
            return True
    return False

def get_problems(mechdb: str) -> typing.List[str]:
    app.open(os.path.join(FILES_PATH, mechdb))
    problems = []
    if (has_weak_springs()):
        problems.append(Problems.WEAK_SPRINGS_ENABLED)
    if (has_rigid_beam()):
        problems.append(Problems.RIGID_REMOTE_POINT_ON_BEAM_CONNECTION)
    if (has_rigid_bearing()):
        problems.append(Problems.RIGID_REMOTE_POINT_ON_BEARING)
    return problems

def report_problems(mechdb: str, problems: typing.List[str]):
    if len(problems) == 0:
        print(f"{mechdb} has no problems")
        return
    print(f"{mechdb} has the following problems:")
    for problem in problems:
        print(f"    {problem}")

def test_mechdbs():
    mechdbs = [file for file in os.listdir(FILES_PATH) if file.endswith(".mechdb")]
    for mechdb in mechdbs:
        problems = get_problems(os.path.join(mechdb))
        report_problems(mechdb, problems)

if __name__ == "__main__":
    try:
        test_mechdbs()
    finally:
        app.new()  # This ensures that there are no leftover lock files